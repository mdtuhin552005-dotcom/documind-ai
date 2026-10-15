import logging

from app.core.config import settings


def configure_logging() -> None:
    level = getattr(logging, settings.log_level.upper(), None)
    if not isinstance(level, int):
        raise ValueError(f"Invalid LOG_LEVEL: {settings.log_level}")

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
