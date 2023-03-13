from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from ..validate_funtions import validate_email
from .. import schemas, models, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=schemas.Token)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    validate_email(user_credentials.username)
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    access_token = oauth2.create_access_token(
        data={"user_id": str(user.id), "user_email": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}
