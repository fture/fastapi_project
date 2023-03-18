from .. import models, utils, schemas, validate_funtions, oauth2
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from ..database import get_db
from uuid import uuid4
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    validate_funtions.validate_uuid(vote.post_id)
    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not exist"
        )
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    target_vote = vote_query.first()
    # dir ==1 for 생성
    if vote.dir == 1:
        if target_vote:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"msg": "You already voted for this post"},
            )
        new_vote = models.Vote(
            post_id=vote.post_id,
            user_id=current_user.id,
            like=vote.like,
            comment=vote.comment,
        )
        db.add(new_vote)
        db.commit()
        return {"msg": "Your vote added for this post"}
    # else for 삭제 및 유효성 검사
    else:
        if not target_vote:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={"msg": "Invalid Vote"}
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"msg": "Your vote deleted"}
