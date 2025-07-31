from sqlmodel import SQLModel, Field
from sqlalchemy import Column, JSON

class Query(SQLModel, table=True):
    id: str = Field(primary_key=True)
    query: str

class Metric(SQLModel, table=True):
    id: str = Field(primary_key=True)
    query_id: str = Field(foreign_key="query.id")
    is_editable: bool = Field(default=True)

class Layout(SQLModel, table=True):
    metric_id: str = Field(primary_key=True)
    layout_json: dict = Field(sa_column=Column(JSON))
