from sqlmodel import create_engine, Session

engine = create_engine("postgresql://postgres:admin@localhost:5432/intropy-test", echo=True)

def get_session():
    return Session(engine)
