from src.models import MetricDefinition, Query, Metrics
from sqlmodel import Session, select
from fastapi import HTTPException
from sqlalchemy import text

def get_metric_data(session: Session, metric_id: str):
    metric_def = session.exec(select(MetricDefinition).where(MetricDefinition.id == metric_id)).first()
    if not metric_def:
        raise HTTPException(status_code=404, detail="Metric not found")
    query_obj = session.exec(select(Query).where(Query.id == metric_def.query_id)).first()
    if not query_obj:
        raise HTTPException(status_code=404, detail="Query not found for this metric")
    # Execute the SQL query stored in the Query table
    result = session.exec(text(query_obj.query)).mappings()
    rows = [dict(row) for row in result]
    return {"metric_id": metric_id, "data": rows}
