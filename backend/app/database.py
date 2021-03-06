from sqlmodel import SQLModel, create_engine, Session
from app.core import config

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=config.ECHO_DATABASE, connect_args=connect_args)


def create_db_and_tables():  # pragma: no cover
    SQLModel.metadata.create_all(engine)


def get_session():  # pragma: no cover
    with Session(engine) as session:
        yield session
