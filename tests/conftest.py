from fastapi.testclient import TestClient
from sqlalchemy import URL
from sqlmodel import create_engine, Session, SQLModel, select
import pytest

from app.main import app
from app.config import settings
from app.database import get_session
from app.oauth2 import create_access_token
from app import models


#url params
url_object = URL.create(
    'postgresql',
    username = settings.database_username,
    password = settings.database_password,
    host = settings.database_host,
    port = settings.database_port,
    database = settings.database_name+'_test',
)

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(url_object, echo=False)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "kyle@gmail.com",
        "password": "password"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {
        "email": "jim@gmail.com",
        "password": "password"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers.update({'Authorization': f'Bearer {token}'})
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id'],
        },
        {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user['id'],
        },
        {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user['id'],
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user2['id'],
        }
    ]


    post_map = list(map(lambda post: models.Post(**post), posts))
    session.add_all(post_map)
    session.commit()
    posts = session.exec(select(models.Post)).all()
    return posts