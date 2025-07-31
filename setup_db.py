"""
setup_db.py
------------
Database initialization and sample data loading script.
- Handles DB schema creation
- Loads queries, metrics, layouts, and metric data from CSV/JSON
- Cleans and validates data before insert
- Designed for clarity, efficiency, and maintainability
"""
import logging
import math
from datetime import date
import csv
import json
import pandas as pd
from sqlmodel import SQLModel, Session, select
from src.config import settings
from src.db import engine
from src.models import MetricDefinition, Query, Layout, Metrics

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- Utility Functions ---
def to_float(val):
    try:
        if pd.isnull(val) or (isinstance(val, float) and math.isnan(val)):
            return None
        return float(val)
    except (TypeError, ValueError):
        return None

def to_int(val):
    try:
        if pd.isnull(val) or (isinstance(val, float) and math.isnan(val)):
            return None
        return int(val)
    except (TypeError, ValueError):
        return None

def to_date(val):
    try:
        return date.fromisoformat(val)
    except Exception:
        return None

# --- Data Cleaning ---
def clean_metric_data(df):
    required_cols = ['id', 'date']
    df = df.dropna(subset=required_cols)
    df['obsolescence'] = df['obsolescence'].apply(to_float)
    df['parts_flagged'] = df['parts_flagged'].apply(to_int)
    df['obsolescence_val'] = df['obsolescence_val'].apply(to_float)
    df['date'] = df['date'].apply(to_date)
    df = df.dropna(subset=['date'])
    return df

# --- DB Operations ---
def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)
    logging.info("Database schema and tables created successfully.")

def insert_queries(session, queries_path=None):
    if queries_path is None:
        queries_path = settings.queries_csv
    try:
        with open(queries_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row.get('id') or not row.get('query'):
                    logging.warning(f"Skipping query row due to missing id or query: {row}")
                    continue
                if not session.get(Query, row['id']):
                    session.add(Query(id=row['id'], query=row['query']))
        logging.info("Queries loaded.")
    except Exception as e:
        logging.error(f"Failed to load queries: {e}")

def insert_metrics_and_layouts(session, metrics_path=None):
    if metrics_path is None:
        metrics_path = settings.metrics_json
    try:
        with open(metrics_path, 'r') as f:
            data = json.load(f)
            for item in data['items']:
                query_id = item.get('queryId') or item.get('query_id')
                if not query_id:
                    logging.warning(f"Skipping metric {item.get('id')} due to missing query_id")
                    continue
                if not session.get(MetricDefinition, item['id']):
                    session.add(MetricDefinition(id=item['id'], query_id=query_id, is_editable=item['isEditable']))
            for layout in data.get('layouts', {}).get('lg', []):
                if not session.get(Layout, layout['i']):
                    session.add(Layout(metric_id=layout['i'], layout_json=json.dumps(layout)))
        logging.info("Metrics and layouts loaded.")
    except Exception as e:
        logging.error(f"Failed to load metrics/layouts: {e}")

def insert_metric_data(session, metric_data_path=None):
    if metric_data_path is None:
        metric_data_path = settings.metric_data_csv
    try:
        df = pd.read_csv(metric_data_path)
        df = clean_metric_data(df)
        df = df.drop_duplicates()  # Deduplicate in-memory

        for _, row in df.iterrows():
            fields = {
                'id': row['id'],
                'date': row['date'],
                'obsolescence': row['obsolescence'] if pd.notnull(row['obsolescence']) else None,
                'alert_type': row['alert_type'] if pd.notnull(row['alert_type']) else None,
                'parts_flagged': row['parts_flagged'] if pd.notnull(row['parts_flagged']) else None,
                'obsolescence_val': row['obsolescence_val'] if pd.notnull(row['obsolescence_val']) else None,
                'alert_category': row['alert_category'] if pd.notnull(row['alert_category']) else None,
            }
            exists = session.exec(
                select(Metrics).where(
                    Metrics.id == fields['id'],
                    Metrics.date == fields['date'],
                    Metrics.obsolescence == fields['obsolescence'],
                    Metrics.alert_type == fields['alert_type'],
                    Metrics.parts_flagged == fields['parts_flagged'],
                    Metrics.obsolescence_val == fields['obsolescence_val'],
                    Metrics.alert_category == fields['alert_category'],
                )
            ).first()
            if not exists:
                metric = Metrics(**fields)
                session.add(metric)
        logging.info("Metric data loaded (deduplicated).")
    except Exception as e:
        logging.error(f"Failed to load metric data: {e}")

# --- Main Orchestration ---
def load_sample_data(engine):
    with Session(engine) as session:
        insert_queries(session)
        insert_metrics_and_layouts(session)
        insert_metric_data(session)
        session.commit()
        logging.info("Sample data loaded successfully.")

if __name__ == "__main__":
    create_db_and_tables(engine)
    load_sample_data(engine)
