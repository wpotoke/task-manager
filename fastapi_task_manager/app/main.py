# pylint:disable=no-member
import uvicorn
import fastapi
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.utils.exceptions.database import EntityDoesNotExist

from app.api.endpoints import router as api_router
from app.config.events import (
    execute_backend_server_event_handler,
    terminate_backend_server_event_handler,
)
from app.config.manager import settings


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI(**settings.set_backend_app_attributes)

    @app.exception_handler(EntityDoesNotExist)
    async def entity_not_found_exception_handler(request, exc: EntityDoesNotExist):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    app.add_event_handler(
        "startup",
        execute_backend_server_event_handler(backend_app=app),
    )
    app.add_event_handler(
        "shutdown",
        terminate_backend_server_event_handler(backend_app=app),
    )

    app.include_router(router=api_router, prefix=settings.API_PREFIX)

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()

if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.BACKEND_SERVER_HOST,
        port=settings.BACKEND_SERVER_PORT,
        reload=settings.DEBUG,
        workers=settings.BACKEND_SERVER_WORKERS,
        log_level=settings.LOGGING_LEVEL,
    )
