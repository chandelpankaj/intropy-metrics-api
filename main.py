import sys
sys.path.append("src")

from fastapi import FastAPI
import structlog
from src.routes import metrics, health
from src.utils.exceptions import register_exception_handlers

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

# Register exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(health.router, prefix="", tags=["Health"])
app.include_router(metrics.router, prefix="", tags=["Metrics"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
