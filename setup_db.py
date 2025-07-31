from sqlmodel import SQLModel, create_engine, Session
from models import Metric, Query, Layout
import json
import csv
from pathlib import Path

DATABASE_URL = "postgresql://postgres:admin@localhost:5432/intropy-test"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    print("Database schema and tables created successfully.")

def load_sample_data():
    # Load queries
    queries_path = Path(__file__).parent / 'data' / 'queries.csv'
    with open(queries_path, 'r') as f:
        reader = csv.DictReader(f)
        queries = [Query(id=row['id'], query=row['query']) for row in reader]
    # Load metrics and layouts
    metrics_path = Path(__file__).parent / 'data' / 'metrics.json'
    with open(metrics_path, 'r') as f:
        data = json.load(f)
        metrics = []
        for item in data['items']:
            query_id = item.get('queryId') or item.get('query_id')
            if not query_id:
                print(f"Skipping metric {item.get('id')} due to missing query_id")
                continue
            metrics.append(Metric(id=item['id'], query_id=query_id, is_editable=item['isEditable']))
        # Load layouts for 'lg' breakpoint (you can store the whole layouts dict if you want)
        layouts = []
        for layout in data.get('layouts', {}).get('lg', []):
            layouts.append(Layout(metric_id=layout['i'], layout_json=json.dumps(layout)))
    # Insert into DB
    with Session(engine) as session:
        for query in queries:
            if not session.get(Query, query.id):
                session.add(query)
        for metric in metrics:
            if not session.get(Metric, metric.id):
                session.add(metric)
        for layout in layouts:
            if not session.get(Layout, layout.metric_id):
                session.add(layout)
        session.commit()
    print("Sample data loaded successfully.")

if __name__ == "__main__":
    create_db_and_tables()
    load_sample_data()
