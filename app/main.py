from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api_router import api_router as api_router_v1
from app.core.config import settings
from app.core.exceptions import validation_exception_handler
from app.core.migrations import run_migrations


run_migrations()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)


app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
    expose_headers=["X-Process-Time"],
    max_age=3600,
)


app.include_router(
    api_router_v1,
    prefix=settings.API_PREFIX,
)


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> dict[str, str]:
    return {
        "message": "DocDigitales Test running",
    }
