from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import SessionDep

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=models.UserPublic)
def create_user(user: models.UserCreate, session: SessionDep):
    #hash password from user.password
    hashed_pwd = utils.hash_pwd(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=models.UserPublic)
def get_user(id: int, session: SessionDep):
    user = session.query(models.User).get(id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} not found")
    return user
