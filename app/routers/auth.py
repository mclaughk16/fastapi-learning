from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import Session, SQLModel, select


from .. import models, utils, oauth2
from ..database import SessionDep

router = APIRouter(prefix="/login",
                   tags=['Auth'])

@router.post("/", response_model=models.Token)
def login(session: SessionDep, user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = session.exec(select(models.User).where(models.User.email == user_credentials.username)).first()


    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")

    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}