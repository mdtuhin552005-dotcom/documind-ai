import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.api.routes import auth, chat, documents, health, admin
from app.core.config import Settings, settings
from app.core.logging import configure_logging
from app.database import DocumentDatabase
from app.services.chat import ChatService
from app.services.documents import DocumentService

logger = logging.getLogger(__name__)
APP_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    configure_logging()
    configured_settings: Settings = application.state.settings
    configured_settings.data_dir.mkdir(parents=True, exist_ok=True)
    configured_settings.uploads_dir.mkdir(parents=True, exist_ok=True)
    configured_settings.chroma_dir.mkdir(parents=True, exist_ok=True)

    database = DocumentDatabase(configured_settings.database_path)
    await database.initialize()
    embeddings = (
        GoogleGenerativeAIEmbeddings(
            model=configured_settings.embedding_model,
            google_api_key=configured_settings.gemini_api_key.get_secret_value(),
            max_retries=2,
        )
        if configured_settings.gemini_api_key
        and configured_settings.gemini_api_key.get_secret_value()
        else None
    )
    vector_store = Chroma(
        collection_name="documind_documents",
        persist_directory=str(configured_settings.chroma_dir),
        embedding_function=embeddings,
    )
    application.state.database = database
    application.state.vector_store = vector_store
    application.state.document_service = DocumentService(
        configured_settings,
        database,
        vector_store,
    )
    application.state.chat_service = ChatService(
        configured_settings,
        database,
        vector_store,
    )
    logger.info("DocuMind AI started with data directory %s", configured_settings.data_dir)
    yield
    logger.info("DocuMind AI stopped")


def create_app(configured_settings: Settings = settings) -> FastAPI:
    application = FastAPI(
        title="DocuMind AI",
        description="Ask questions about your PDFs and get answers with page citations.",
        version="1.0.0",
        lifespan=lifespan,
    )
    application.state.settings = configured_settings
    if configured_settings.cors_origins:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=configured_settings.cors_origins,
            allow_credentials=False,
            allow_methods=["GET", "POST", "DELETE"],
            allow_headers=["Content-Type"],
        )

    application.include_router(auth.router)
    application.include_router(documents.router)
    application.include_router(chat.router)
    application.include_router(chat.conversations_router)
    application.include_router(health.router)
    application.include_router(admin.router)
    application.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")

    @application.exception_handler(StarletteHTTPException)
    async def http_error_handler(
        request: Request,
        error: StarletteHTTPException,
    ) -> JSONResponse:
        if request.url.path.startswith("/api/"):
            detail = error.detail if isinstance(error.detail, str) else "The request could not be completed."
            return JSONResponse(
                status_code=error.status_code,
                content={"detail": detail},
                headers=error.headers,
            )
        return JSONResponse(status_code=error.status_code, content={"detail": error.detail})

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        error: RequestValidationError,
    ) -> JSONResponse:
        logger.info("Request validation failed on %s: %s", request.url.path, error.errors())
        return JSONResponse(
            status_code=422,
            content={"detail": "The request contains invalid or missing fields."},
        )

    @application.exception_handler(Exception)
    async def unexpected_error_handler(request: Request, error: Exception) -> JSONResponse:
        logger.exception(
            "Unhandled error for %s %s: %s",
            request.method,
            request.url.path,
            error,
        )
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected server error occurred."},
        )

    @application.get("/", include_in_schema=False)
    async def home() -> FileResponse:
        return FileResponse(APP_DIR / "templates" / "index.html")

    @application.post("/register", include_in_schema=False, status_code=201)
    @application.post("/signup", include_in_schema=False, status_code=201)
    async def root_register(
        request: Request,
        response: Response,
        payload: auth.UserRegisterRequest,
    ) -> auth.AuthResponse:
        return await auth.register(request, response, payload)

    @application.post("/login", include_in_schema=False)
    async def root_login(
        request: Request,
        response: Response,
        payload: auth.UserLoginRequest,
    ) -> auth.AuthResponse:
        return await auth.login(request, response, payload)

    @application.post("/google", include_in_schema=False)
    async def root_google(
        request: Request,
        response: Response,
        payload: auth.GoogleCredentialRequest,
    ) -> auth.AuthResponse:
        return await auth.google_auth(request, response, payload)

    return application


app = create_app()
