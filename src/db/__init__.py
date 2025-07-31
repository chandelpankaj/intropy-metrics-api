from sqlmodel import create_engine, Session
from src.config import settings

engine = create_engine(settings.database_url, echo=True)

def get_session():
    return Session(engine)
