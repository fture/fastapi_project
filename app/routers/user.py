from .. import models, utils, schemas, validate_funtions
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from ..database import get_db
from uuid import uuid4
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    validate_funtions.validate_email(user.email)
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    user.password = utils.hash(user.password)
    new_user = models.User(id=uuid4(), **user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.User)
async def read_user(id: str, db: Session = Depends(get_db)):
    validate_funtions.validate_uuid(id)
    target_user = db.query(models.User).filter(models.User.id == id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    return target_user
