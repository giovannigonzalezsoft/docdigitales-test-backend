from fastapi import FastAPI, status

from app.core.config import settings
from app.core.migrations import run_migrations


run_migrations()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> dict[str, str]:
    return {
        "message": "DocDigitales Test running",
    }