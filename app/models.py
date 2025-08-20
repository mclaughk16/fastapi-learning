from sqlalchemy import Column, String, Integer, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Annotated

#SQLModel models (new for FastAPI applications)
class UserBase(SQLModel):
    email: EmailStr = Field(nullable=False, unique=True)

class UserCreate(UserBase):
    password: str = Field(nullable=False)

class User(UserCreate, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')))

class UserPublic(UserBase):
    id: int
    created_at: datetime


class PostBase(SQLModel):
    title: str = Field(nullable=False)
    content: str = Field(nullable=False)
    published: bool = Field(default=True, nullable=False)

class Post(PostBase, table = True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)
    created_at: datetime = Field(sa_column=Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()')))
    owner_id: int | None = Field(default=None, foreign_key="user.id", ondelete="CASCADE", nullable=False)
    #Relationship to user.id

class PostVote(SQLModel):
    Post: Post
    votes: int



class VoteCreate(SQLModel):
    post_id: int
    dir: int = Field(Annotated[int, Field(le=1, ge=0)])

class Vote(SQLModel, table=True):
    user_id: int = Field(foreign_key='user.id', ondelete = "CASCADE", primary_key=True)
    post_id: int = Field(foreign_key='post.id', ondelete = "CASCADE", primary_key=True)

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    id: str


#Standard SQLAlchemy models
"""
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default= 'TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey('users.id', ondelete = "CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey('users.id', ondelete = "CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)

"""