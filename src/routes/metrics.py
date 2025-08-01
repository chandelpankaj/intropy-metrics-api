from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.db import get_session
from src.schemas.metrics import MetricDataResponse, MetricCreateRequest, MetricCreateResponse
from src.services.metrics_service import get_metric_data, create_metric_service

router = APIRouter()

@router.get(
    "/metrics/{metric_id}",
    response_model=MetricDataResponse,
    tags=["Metrics"],
    summary="Get Metric Data",
    response_description="Metric data for the given metric ID",
    responses={
        404: {"description": "Metric or query not found"},
        500: {"description": "Internal server error"}
    },
)
async def get_metric(
    metric_id: str,
    session: Session = Depends(get_session)
):
    """
    Retrieve metric data for a given metric ID.
    - **metric_id**: The unique identifier of the metric definition.
    Returns metric data as a list of records.
    """
    return get_metric_data(session, metric_id)

@router.post(
    "/metrics",
    response_model=MetricCreateResponse,
    tags=["Metrics"],
    summary="Create a new metric (Mock AI)",
    status_code=201,
    responses={
        201: {"description": "Metric created successfully"},
        400: {"description": "Invalid request"},
        500: {"description": "Internal server error"}
    }
)
async def create_metric(
    request: MetricCreateRequest,
    session: Session = Depends(get_session)
):
    """
    Accepts user input, simulates LLM-generated SQL, stores new metric & query.
    """
    return create_metric_service(session, request.name, request.description)
