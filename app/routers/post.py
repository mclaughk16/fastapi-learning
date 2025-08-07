from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate,
                 db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), limit: int = 10, offset: int = 0, search: Optional[str] = None):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    return posts

@router.get("/id/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    return post

@router.get("/user/{user_id}", response_model=List[schemas.PostResponse])
def get_user_posts(user_id: int, db: Session = Depends(get_db)):
    user_posts = db.query(models.Post).filter(models.Post.owner_id == user_id)
    return user_posts

@router.get("/owned", response_model=List[schemas.PostResponse])
def get_owned_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    owned_posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id)
    return owned_posts


@router.delete("/{id}")
def delete_post(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_q = db.query(models.Post).filter(models.Post.id == id)
    post = post_q.first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    if current_user.id != post.owner_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform requested action")

    post_q.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int,
                updated_post: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    post_q = db.query(models.Post).filter(models.Post.id == id)
    post = post_q.first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")
    if current_user.id != post.owner_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="You are not authorized to perform requested action")
    post_q.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post