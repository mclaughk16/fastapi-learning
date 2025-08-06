from typing import Optional, List

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine, text, URL, MetaData, Table, Column, String, Integer, Boolean, TIMESTAMP, False_, \
    select, FetchedValue, insert, delete, update
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
import datetime
from . import models, schemas, utils
from .database import engine, get_db
from .schemas import PostResponse
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to the API"}