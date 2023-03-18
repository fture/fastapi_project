from typing import List, Optional

from sqlalchemy import func
from .. import models, schemas, validate_funtions, oauth2
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db
from uuid import uuid4
from sqlalchemy.orm import Session


router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostOut])
async def read_posts(
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
    limit: int = 5,
    skip: int = 0,
    serch: Optional[str] = "",
):
    posts = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(serch))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(
    post: schemas.PostBase,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    new_post = models.Post(
        id=uuid4(),
        owner_id=current_user.id,
        owner_email=current_user.email,
        **post.dict()
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{posts_id}", status_code=status.HTTP_200_OK, response_model=schemas.PostOut)
async def read_post(posts_id: str, db: Session = Depends(get_db)):
    validate_funtions.validate_uuid(posts_id)
    target_post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == posts_id)
        .first()
    )

    if not target_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )

    return target_post


@router.delete("/{posts_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    posts_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    validate_funtions.validate_uuid(posts_id)
    target_post = db.query(models.Post).filter(models.Post.id == posts_id)

    if not target_post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if target_post.first().owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this post",
        )
    target_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT, content="Post deleted")


@router.put("/{posts_id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
async def update_post(
    posts_id: str,
    post: schemas.PostBase,
    db: Session = Depends(get_db),
    current_user: str = Depends(oauth2.get_current_user),
):
    validate_funtions.validate_uuid(posts_id)
    post_query = db.query(models.Post).filter(models.Post.id == posts_id)
    target_post = post_query.first()

    if not target_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    if target_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to delete this post",
        )
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
