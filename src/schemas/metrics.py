from typing import List, Any, Dict

from pydantic import BaseModel


class MetricCreateRequest(BaseModel):
    name: str
    description: str


class MetricCreateResponse(BaseModel):
    metric_id: str
    query_id: str
    sql: str


class MetricDataResponse(BaseModel):
    metric_id: str
    data: List[Dict[str, Any]]
