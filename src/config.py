from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    database_url: str
    data_dir: str = str(Path(__file__).parent.parent / "data")
    queries_csv: str = str(Path(data_dir) / "queries.csv")
    metrics_json: str = str(Path(data_dir) / "metrics.json")
    metric_data_csv: str = str(Path(data_dir) / "metric_data.csv")

    class Config:
        env_file = ".env-local"

settings = Settings()
