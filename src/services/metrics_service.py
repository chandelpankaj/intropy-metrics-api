from src.models import MetricDefinition, Query, Metrics
from sqlmodel import Session, select
from src.exceptions import NotFoundException
from sqlalchemy import text
from uuid import uuid4


def get_metric_data(session: Session, metric_id: str):
    metric_def = session.exec(select(MetricDefinition).where(MetricDefinition.id == metric_id)).first()
    if not metric_def:
        raise NotFoundException("Metric not found", details={"metric_id": metric_id})
    query_obj = session.exec(select(Query).where(Query.id == metric_def.query_id)).first()
    if not query_obj:
        raise NotFoundException("Query not found for this metric",
                                details={"metric_id": metric_id, "query_id": metric_def.query_id})
    # Execute the SQL query stored in the Query table
    result = session.exec(text(query_obj.query)).mappings()
    rows = [dict(row) for row in result]
    return {"metric_id": metric_id, "data": rows}


def create_metric_service(session, name: str, description: str):
    """
    Simulates LLM-generated SQL, stores new Query and MetricDefinition, returns their IDs and SQL.
    Uses simple SQL patterns similar to existing queries.
    """

    simulated_sql = f"""
    SELECT 
        DATE(date) AS day,
        SUM(obsolescence) AS cost_avoided
    FROM metrics
    WHERE id = '{name.lower().replace(' ', '_')}'
      AND date >= CURRENT_DATE - INTERVAL '30' DAY
    GROUP BY DATE(date)
    ORDER BY day;
    """
    
    # Create and store the query first
    query_id = str(uuid4())
    query_obj = Query(id=query_id, query=simulated_sql)
    session.add(query_obj)
    session.flush()  # Flush to get the ID without committing the transaction
    
    # Now create the metric definition with the existing query_id
    metric_id = str(uuid4())
    metric_def = MetricDefinition(
        id=metric_id, 
        query_id=query_id, 
        is_editable=True,
        name=name,
        description=description
    )
    session.add(metric_def)
    
    session.commit()  # Now commit both objects together
    return {"metric_id": metric_id, "query_id": query_id, "sql": simulated_sql}
