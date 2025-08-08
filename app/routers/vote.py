from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import models, schemas, oauth2, database
from ..database import SessionDep

router = APIRouter(prefix="/vote",
                   tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: models.VoteCreate,
         session: SessionDep,
         current_user: int = Depends(oauth2.get_current_user)):
    post_q = session.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post_q:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} not found")
    vote_q = session.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                          models.Vote.user_id == current_user.id)
    found_vote = vote_q.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail = f"User {current_user} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id,
                               user_id=current_user.id)
        session.add(new_vote)
        session.commit()
        return {"message": "vote successful!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail = "Vote does not exist")
        vote_q.delete(synchronize_session=False)
        session.commit()
        return {"message": "vote removed successfully!"}

