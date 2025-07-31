from src.models import MetricDefinition, Query, Metrics
from sqlmodel import Session, select
from src.exceptions import NotFoundException
from sqlalchemy import text

def get_metric_data(session: Session, metric_id: str):
    metric_def = session.exec(select(MetricDefinition).where(MetricDefinition.id == metric_id)).first()
    if not metric_def:
        raise NotFoundException("Metric not found", details={"metric_id": metric_id})
    query_obj = session.exec(select(Query).where(Query.id == metric_def.query_id)).first()
    if not query_obj:
        raise NotFoundException("Query not found for this metric", details={"metric_id": metric_id, "query_id": metric_def.query_id})
    # Execute the SQL query stored in the Query table
    result = session.exec(text(query_obj.query)).mappings()
    rows = [dict(row) for row in result]
    return {"metric_id": metric_id, "data": rows}
