import sys
sys.path.append("src")

from fastapi import FastAPI, Path, Request
from fastapi.responses import JSONResponse
from src.db import get_session
from src.services.metrics_service import get_metric_data
from src.exceptions import AppException
import structlog
from typing import List, Dict, Any
from pydantic import BaseModel

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),

    cache_logger_on_first_use=True,
)

log = structlog.get_logger()

class MetricDataResponse(BaseModel):
    metric_id: str
    data: List[Dict[str, Any]]

# FastAPI app
app = FastAPI(
    title="Customer API",
    version="0.1.0"
)

# Exception Handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    log.error("AppException", code=exc.code, message=exc.message, details=exc.details, path=request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    log.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.get("/", tags=["Health"], summary="API Status", response_description="API status message")
async def root():
    """Health and status endpoint. Returns a simple status message to verify the API is running."""
    return {"message": "Customer API", "status": "running"}

@app.get("/health", tags=["Health"], summary="Health Check", response_description="Health check status")
def health_check():
    """Simple health check endpoint. Returns 'ok' if the API is healthy."""
    return {"status": "ok"}

@app.get(
    "/metrics/{metric_id}",
    tags=["Metrics"],
    summary="Get Metric Data",
    response_model=MetricDataResponse,
    response_description="Metric data for the given metric ID",
    responses={
        404: {"description": "Metric or query not found"},
        500: {"description": "Internal server error"}
    },
)
def get_metric(
    metric_id: str = Path(
        ...,
        title="The ID of the metric to retrieve",
        min_length=1,
        max_length=64,
        example="metric_123"
    )
):
    """Retrieve metric data for a given metric ID.
    - **metric_id**: The unique identifier of the metric definition.
    Returns metric data as a list of records."""
    try:
        with get_session() as session:
            return get_metric_data(session, metric_id)
    except Exception as exc:
        log.error("Error in /metrics/{metric_id}", error=str(exc), metric_id=metric_id)
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)