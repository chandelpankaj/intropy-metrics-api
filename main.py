import sys
sys.path.append("src")

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.exceptions import AppException
import structlog
from src.routes import metrics, health

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

# Create FastAPI app
app = FastAPI(
    title="Customer API",
    version="0.1.0"
)

# Include routers
app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(metrics.router, prefix="", tags=["Metrics"])

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
