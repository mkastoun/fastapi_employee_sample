import uvicorn

import fastapi_sqla
from fastapi import FastAPI
from structlog import get_logger
from app import settings
from app.core.models import HealthCheck
from app.router.api_v1.endpoints import api_router

log = get_logger()

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    debug=settings.debug
)

fastapi_sqla.setup(app)


@app.get("/health", response_model=HealthCheck, tags=["status"])
def health():
    """
    health endpoint responsible to return the application status check
    Returns:
          Returns json response with the name,version and description of the app
    """
    return {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description
    }

app.include_router(api_router, prefix=settings.api_v1_prefix)


if __name__ == '__main__':
   uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)
