from typing import List
from .. import models, schemas, validate_funtions, oauth2
from fastapi import Depends, HTTPException, status, APIRouter
from ..database import get_db
from uuid import uuid4
from sqlalchemy.orm import Session


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.Post])
async def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    post: schemas.PostBase,
    db: Session = Depends(get_db),
    get_current_user: oauth2.get_current_user = Depends(oauth2.get_current_user),
):
    new_post = models.Post(id=uuid4(), **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def read_post(id: str, db: Session = Depends(get_db)):
    validate_funtions.validate_uuid(id)
    target_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not target_post:
        raise HTTPException(status_code=404, detail="Post not found")

    return target_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: str,
    db: Session = Depends(get_db),
    get_current_user: oauth2.get_current_user = Depends(oauth2.get_current_user),
):
    validate_funtions.validate_uuid(id)
    target_post = db.query(models.Post).filter(models.Post.id == id)

    if not target_post.first():
        raise HTTPException(status_code=404, detail="Post not found")
    target_post.delete(synchronize_session=False)
    db.commit()

    return {"delete_success": "ok"}


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(
    id: str,
    post: schemas.PostBase,
    db: Session = Depends(get_db),
    get_current_user: oauth2.get_current_user = Depends(oauth2.get_current_user),
):
    validate_funtions.validate_uuid(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    read_posts = post_query.first()

    if not read_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
