from fastapi import APIRouter, Request

from app.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/api/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    configured = request.app.state.settings.gemini_api_key
    return HealthResponse(
        status="ok",
        ai_configured=bool(configured and configured.get_secret_value()),
    )
