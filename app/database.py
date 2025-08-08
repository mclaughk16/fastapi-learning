from sqlalchemy import URL
from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends
from .config import settings
from . import models

#url params
url_object = URL.create(
    'postgresql',
    username = settings.database_username,
    password = settings.database_password,
    host = settings.database_host,
    port = settings.database_port,
    database = settings.database_name,
)

#create engine
engine = create_engine(url_object, echo = True)

# create db and tables
def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)

#create session
def get_session():
    with Session(engine) as session:
        yield session

#create session dependency
SessionDep = Annotated[Session, Depends(get_session)]
