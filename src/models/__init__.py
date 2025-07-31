from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON
from datetime import date
from typing import Optional
import uuid

class Query(SQLModel, table=True):
    id: str = Field(primary_key=True)
    query: str

class MetricDefinition(SQLModel, table=True, table_name="metric_definition"):
    id: str = Field(primary_key=True)
    query_id: str = Field(foreign_key="query.id")
    is_editable: bool = Field(default=True)

class Metrics(SQLModel, table=True):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    id: str
    date: date
    obsolescence: Optional[float] = None
    alert_type: Optional[str] = None
    parts_flagged: Optional[int] = None
    obsolescence_val: Optional[float] = None
    alert_category: Optional[str] = None
    # Extendable for future metric columns

class Layout(SQLModel, table=True):
    metric_id: str = Field(primary_key=True)
    layout_json: dict = Field(sa_column=Column(JSON))
