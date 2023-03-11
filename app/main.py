from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
from . import models
from .database import Base, get_db, engine
from uuid import uuid4, UUID
from sqlalchemy.orm import Session


Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="/.,asd][p123",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connected to database")
        break
    except Exception as error:
        print("failed connecting to database")
        print("Error")
        sleep(2)


def validate_uuid(value):
    try:
        return UUID(value)
    except ValueError:
        raise HTTPException(status_code=400, detail="Not a valid UUID")


@app.get("/posts")
async def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute(""" SELECT * FROM posts; """)
    # posts = cursor.fetchall()

    return {"data": posts}


@app.post("/posts")
async def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(id=uuid4(), **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # cursor.execute(
    #     " INSERT INTO posts(id, title, content, published) VALUES (%s,%s, %s, %s) RETURNING * ",
    #     (uuid4(), post.title, post.content, post.published),
    # )
    # new_posts = cursor.fetchone()
    # conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
async def read_post(id: str, db: Session = Depends(get_db)):
    validate_uuid(id)
    target_post = db.query(models.Post).filter(models.Post.id == id).first()

    # cursor.execute(""" SELECT * FROM posts WHERE id=%s; """, (id,))
    # target_post = cursor.fetchone()
    if not target_post:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"data": target_post}


@app.delete("/posts/{id}")
async def delete_post(id: str, db: Session = Depends(get_db)):
    validate_uuid(id)
    target_post = db.query(models.Post).filter(models.Post.id == id)

    # cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING title; """, (id,))
    # target_post = cursor.fetchone()

    # conn.commit()
    if not target_post.first():
        raise HTTPException(status_code=404, detail="Post not found")
    target_post.delete(synchronize_session=False)
    db.commit()
    return {"delete_success": "ok"}


@app.put("/posts/{id}")
async def update_post(id: str, post: Post, db: Session = Depends(get_db)):
    validate_uuid(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    read_posts = post_query.first()
    # cursor.execute(
    #     """ UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *; """,
    #     (post.title, post.content, post.published, id),
    # )
    # update_post = cursor.fetchone()
    if not read_post:
        raise HTTPException(status_code=404, detail="Post not found")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return {"update_success": post_query.first()}
