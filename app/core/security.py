import hashlib
import hmac
import secrets


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
    return f"{salt}:{digest.hex()}"


def verify_password(password: str, hashed: str) -> bool:
    try:
        salt, key = hashed.split(":", 1)
        digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000)
        return hmac.compare_digest(digest.hex(), key)
    except Exception:
        return False


def generate_token() -> str:
    return secrets.token_urlsafe(32)
