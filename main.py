from fastapi import Path
import structlog
from fastapi import FastAPI
from fastapi import Path
from sqlmodel import create_engine, Session

from src.services.metrics_services import get_metric_data

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

# Database configuration
DATABASE_URL = "postgresql://postgres:admin@localhost:5432/intropy-test"

# Create engine only when needed (not during imports for Alembic)
def get_engine():
    return create_engine(DATABASE_URL, echo=True)

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

# FastAPI app
app = FastAPI(title="Customer API", version="0.1.0")

@app.get("/")
async def root():
    return {"message": "Customer API", "status": "running"}

@app.get("/health", tags=["Health"], summary="Health Check", response_description="Health check status")
def health_check():
    """Simple health check endpoint. Returns 'ok' if the API is healthy."""
    return {"status": "ok"}

@app.get("/metrics/{metric_id}")
def get_metric(metric_id: str = Path(..., title="The ID of the metric to retrieve")):
    """Retrieve metric data for a given metric ID."""
    engine = get_engine()
    with Session(engine) as session:
        return get_metric_data(session, metric_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)