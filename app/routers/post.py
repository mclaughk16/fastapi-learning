from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from typing import List, Optional
import pydantic
import json

from .. import models, schemas, oauth2
from ..database import SessionDep

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.Post)
def create_posts(post: models.PostBase,
                 session: SessionDep,
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)

    return new_post

#@router.get("/")
@router.get("/", response_model=List[models.PostVote])
def get_posts(session: SessionDep, limit: int = 10, offset: int = 0, search: Optional[str] = ""):
    #posts = session.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()

    results = session.exec(select(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(offset)).all()
    response = []
    for post, votes in results:
        print("Post:", post, "Votes:", votes)
        result = {"Post": post, "votes": votes}
        response.append(result)

    return response



@router.get("/id/{id}", response_model=models.PostVote)
def get_post(id: int, session: SessionDep):
    results = session.exec(select(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, isouter=True).group_by(models.Post.id).filter(models.Post.id == id))
    response = []
    for post, votes in results:
        print("Post:", post, "Votes:", votes)
        result = {"Post": post, "votes": votes}
        response.append(result)

    if not results:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return response[0]

@router.get("/user/{user_id}", response_model=List[schemas.PostBase])
def get_user_posts(user_id: int, session: SessionDep):
    user_posts = session.query(models.Post).filter(models.Post.owner_id == user_id)
    return user_posts

@router.get("/owned", response_model=List[schemas.PostBase])
def get_owned_posts(session: SessionDep, current_user: int = Depends(oauth2.get_current_user)):
    owned_posts = session.query(models.Post).filter(models.Post.owner_id == current_user.id)
    return owned_posts


@router.delete("/{id}")
def delete_post(id: int,
                session: SessionDep,
                current_user: int = Depends(oauth2.get_current_user)):
    post_q = session.query(models.Post).filter(models.Post.id == id)
    post = post_q.first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    if current_user.id != post.owner_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform requested action")

    post_q.delete(synchronize_session=False)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostBase)
def update_post(id: int,
                updated_post: models.Post,
                session: SessionDep,
                current_user: int = Depends(oauth2.get_current_user)):
    post_q = session.query(models.Post).filter(models.Post.id == id)
    post = post_q.first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    if current_user.id != post.owner_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform requested action")
    post_q.update(updated_post.model_dump(), synchronize_session=False)
    session.commit()
    return post