from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["Health"], summary="API Status")
async def root():
    """Health and status endpoint. Returns a simple status message to verify the API is running."""
    return {"message": "Customer API", "status": "running"}

@router.get("/health", tags=["Health"], summary="Health Check")
async def health_check():
    """Simple health check endpoint. Returns 'ok' if the API is healthy."""
    return {"status": "ok"}
