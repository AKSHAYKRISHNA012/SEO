from sqlmodel import SQLModel, create_engine, Session
from app.config import settings

# Supports SQLite and PostgreSQL (e.g. postgresql://user:password@localhost/seointel)
engine_kwargs = {}
if settings.DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, echo=False, **engine_kwargs)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
