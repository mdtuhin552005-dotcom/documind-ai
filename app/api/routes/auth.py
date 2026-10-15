import re
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from fastapi import APIRouter, Cookie, Header, HTTPException, Request, Response, status
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2 import id_token
from starlette.concurrency import run_in_threadpool

from app.core.security import generate_token, hash_password, verify_password
from app.database import DocumentDatabase
from app.schemas import AuthResponse, GoogleCredentialRequest, UserLoginRequest, UserRegisterRequest, UserResponse

router = APIRouter(prefix="/api/auth", tags=["authentication"])

EMAIL_REGEX = re.compile(
    r"^[A-Z0-9.!#$%&'*+/=?^_`{|}~-]+"
    r"@[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?"
    r"(?:\.[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?)+$",
    re.IGNORECASE,
)


def _get_database(request: Request) -> DocumentDatabase:
    return request.app.state.database


def _extract_token(
    authorization: str | None = None,
    cookie_token: str | None = None,
) -> str | None:
    if authorization and authorization.lower().startswith("bearer "):
        return authorization[7:].strip()
    return cookie_token


def _verify_google_credential(credential: str, client_id: str) -> dict[str, Any]:
    return id_token.verify_oauth2_token(credential, GoogleRequest(), client_id)


async def require_authenticated_user(request: Request) -> dict[str, Any]:
    token = _extract_token(
        request.headers.get("authorization"),
        request.cookies.get("documind_token"),
    )
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please sign in to continue.")

    database = _get_database(request)
    session = await database.get_session(token)
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your session has expired. Please sign in again.")
    try:
        expires = datetime.fromisoformat(session["expires_at"])
    except (TypeError, ValueError):
        await database.delete_session(token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your session is invalid. Please sign in again.")
    if expires <= datetime.now(UTC):
        await database.delete_session(token)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your session has expired. Please sign in again.")
    return {
        "id": session["user_id"],
        "email": session["email"],
        "full_name": session["full_name"],
        "created_at": session["user_created_at"],
    }


@router.get("/config")
async def auth_config(request: Request) -> dict[str, str | None]:
    return {"google_client_id": request.app.state.settings.google_client_id}


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: Request,
    response: Response,
    payload: UserRegisterRequest,
) -> AuthResponse:
    database = _get_database(request)
    email = payload.email.strip().lower()
    if not EMAIL_REGEX.match(email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Please provide a valid email address.",
        )

    if len(payload.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password must be at least 6 characters long.",
        )

    existing = await database.get_user_by_email(email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists. Please sign in or continue with Google.",
        )

    user_id = str(uuid.uuid4())
    now = datetime.now(UTC).isoformat()
    pwd_hash = hash_password(payload.password)
    user_data = {
        "id": user_id,
        "email": email,
        "password_hash": pwd_hash,
        "full_name": payload.full_name.strip() or email.split("@")[0].capitalize(),
        "created_at": now,
    }
    await database.create_user(user_data)
    try:
        ip = request.client.host if request.client else None
        await database.log_activity("USER_REGISTER", f"Registered: {email}", user_id=user_id, ip_address=ip)
    except Exception:
        pass

    token = generate_token()
    expires_at = (datetime.now(UTC) + timedelta(days=30)).isoformat()
    await database.create_session({
        "token": token,
        "user_id": user_id,
        "created_at": now,
        "expires_at": expires_at,
    })

    response.set_cookie(
        key="documind_token",
        value=token,
        max_age=30 * 86400,
        httponly=True,
        samesite="lax",
        secure=request.url.scheme == "https",
    )

    user_resp = UserResponse(
        id=user_id,
        email=email,
        full_name=user_data["full_name"],
        created_at=now,
    )
    return AuthResponse(
        user=user_resp,
        token=token,
        message="Registration successful. Welcome to DocuMind AI!",
    )


@router.post("/google", response_model=AuthResponse)
async def google_auth(
    request: Request,
    response: Response,
    payload: GoogleCredentialRequest,
) -> AuthResponse:
    client_id = request.app.state.settings.google_client_id
    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Google Sign-In is not configured. Set GOOGLE_CLIENT_ID to enable it.",
        )

    try:
        claims = await run_in_threadpool(
            _verify_google_credential,
            payload.credential,
            client_id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google could not verify this sign-in. Please try again.",
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Google Sign-In is temporarily unavailable. Please try again.",
        ) from error

    email = str(claims.get("email", "")).strip().lower()
    if claims.get("email_verified") is not True or not EMAIL_REGEX.fullmatch(email):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Use a Google account with a verified email address.",
        )

    database = _get_database(request)
    user = await database.get_user_by_email(email)
    now = datetime.now(UTC).isoformat()
    if not user:
        user_id = str(uuid.uuid4())
        pwd_hash = hash_password(str(uuid.uuid4()) + str(uuid.uuid4()))
        full_name = str(claims.get("name") or email.split("@")[0].replace(".", " ").title()).strip()
        user_data = {
            "id": user_id,
            "email": email,
            "password_hash": pwd_hash,
            "full_name": full_name,
            "created_at": now,
        }
        await database.create_user(user_data)
        user = user_data

    token = generate_token()
    expires_at = (datetime.now(UTC) + timedelta(days=30)).isoformat()
    await database.create_session({
        "token": token,
        "user_id": user["id"],
        "created_at": now,
        "expires_at": expires_at,
    })
    try:
        ip = request.client.host if request.client else None
        await database.log_activity("USER_LOGIN_GOOGLE", f"Google Sign-In: {email}", user_id=user["id"], ip_address=ip)
    except Exception:
        pass

    response.set_cookie(
        key="documind_token",
        value=token,
        max_age=30 * 86400,
        httponly=True,
        samesite="lax",
        secure=request.url.scheme == "https",
    )

    user_resp = UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        created_at=user["created_at"],
    )
    return AuthResponse(
        user=user_resp,
        token=token,
        message="Signed in with Google successfully. Welcome to DocuMind AI!",
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    request: Request,
    response: Response,
    payload: UserLoginRequest,
) -> AuthResponse:
    database = _get_database(request)
    email = payload.email.strip().lower()
    user = await database.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found with this email. Please switch to Sign Up or continue with Google.",
        )
    if not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password. Please verify your credentials or sign in with Google.",
        )

    token = generate_token()
    now = datetime.now(UTC).isoformat()
    expires_at = (datetime.now(UTC) + timedelta(days=30)).isoformat()
    await database.create_session({
        "token": token,
        "user_id": user["id"],
        "created_at": now,
        "expires_at": expires_at,
    })
    try:
        ip = request.client.host if request.client else None
        await database.log_activity("USER_LOGIN_PASSWORD", f"Password Sign-In: {email}", user_id=user["id"], ip_address=ip)
    except Exception:
        pass

    response.set_cookie(
        key="documind_token",
        value=token,
        max_age=30 * 86400,
        httponly=True,
        samesite="lax",
        secure=request.url.scheme == "https",
    )

    user_resp = UserResponse(
        id=user["id"],
        email=user["email"],
        full_name=user["full_name"],
        created_at=user["created_at"],
    )
    return AuthResponse(
        user=user_resp,
        token=token,
        message="Signed in successfully. Welcome back!",
    )


@router.get("/me")
async def get_current_user(
    request: Request,
    authorization: str | None = Header(default=None),
    documind_token: str | None = Cookie(default=None),
) -> dict[str, Any]:
    token = _extract_token(authorization, documind_token)
    if not token:
        return {"authenticated": False, "user": None}

    try:
        user = await require_authenticated_user(request)
    except HTTPException:
        return {"authenticated": False, "user": None}

    return {
        "authenticated": True,
        "user": user,
    }


@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    authorization: str | None = Header(default=None),
    documind_token: str | None = Cookie(default=None),
) -> dict[str, str]:
    token = _extract_token(authorization, documind_token)
    if token:
        database = _get_database(request)
        await database.delete_session(token)

    response.delete_cookie(key="documind_token")
    return {"message": "Signed out successfully."}
