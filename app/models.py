from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlmodel import SQLModel, Field

from .database import Base

#Standard SQLAlchemy models

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default= 'TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))




""" SQLModel models (new for FastAPI applications)

class Post(SQLModel, table = True):
    id: int | None = Field(default = None, primary_key=True, nullable=False)
    title: str = Field(nullable = False)
    content: str = Field(nullable = False)
    published: bool = Field(server_default = 'TRUE', nullable=False)
    #created_at: datetime.datetime = Field(nullable = False, server_default=text('now()'))
"""