from sqlalchemy import create_engine, URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#url params
url_object = URL.create(
    'postgresql',
    username = 'postgres',
    password = 'password',
    host = 'localhost',
    port = 5432,
    database = 'fastapi'
)

#create engine
engine = create_engine(url_object, echo = True)

#create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#create session dependency
def get_db(): #session init dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#alt
def get_session():
    with SessionLocal() as session:
        yield session