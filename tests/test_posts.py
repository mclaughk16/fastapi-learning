from typing import List

import pytest

from app import models
from tests.conftest import authorized_client
from sqlmodel import select


def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get('/posts')
    post_map = list(map(lambda post: models.PostVote(**post), response.json()))
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200


def test_get_by_id(client, test_posts):
    response = client.get(f'/posts/id/{test_posts[0].id}')
    post = models.PostVote(**response.json())
    assert post.Post.id == test_posts[0].id
    assert response.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ("new title", "new content", True),
    ("more new title", "more new content", False),
    ("newest title", "newest content", True)
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    response = authorized_client.post("/posts", json={
        "title": title,
        "content": content,
        "published": published,
    })
    created_post = models.Post(**response.json())
    assert response.status_code == 201
    assert created_post.title == title

def test_unauth_user_create_post(client, test_user, test_posts):
    response = client.post("/posts", json={
        "title": "test title",
        "content": "test content",
    })
    assert response.status_code == 401

def test_unauth_user_delete_post(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_delete_post(authorized_client, test_posts, test_user):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204

def test_delete_post_nonexist(authorized_client, test_posts, test_user):
    response = authorized_client.delete(f"/posts/-1")
    assert response.status_code == 404

def test_delete_unowned_post(authorized_client, test_posts, test_user):
    response = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert response.status_code == 403

def test_update_post(authorized_client, test_posts, test_user,session):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
        "owner_id": test_user['id'],
    }
    response = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)

    updated_post = models.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data["title"]

def test_update_unowned_post(authorized_client, test_posts, test_user, test_user2):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
        "owner_id": test_user['id'],
    }
    response = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)

    assert response.status_code == 403

def test_update_post_nonexist(authorized_client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
        "owner_id": test_user['id'],
    }
    response = authorized_client.put(f"/posts/{test_posts[-1].id}", json=data)

    assert response.status_code == 403

def test_unauth_user_update(client, test_posts, test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
        "owner_id": test_user['id'],
    }
    response = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert response.status_code == 401
