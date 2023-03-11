from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
from .models import Post
from .database import Base, get_db, SessionLocal, engine
from uuid import uuid4, UUID
from sqlalchemy.orm import Session

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


Base.metadata.create_all(bind=engine)

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
async def read_posts():
    cursor.execute(""" SELECT * FROM posts; """)
    posts = cursor.fetchall()

    return {"data": posts}


@app.post("/posts")
async def create_post(post: Post):
    cursor.execute(
        " INSERT INTO posts(id, title, content, published) VALUES (%s,%s, %s, %s) RETURNING * ",
        (uuid4(), post.title, post.content, post.published),
    )
    new_posts = cursor.fetchone()
    conn.commit()
    return {"data": new_posts}


@app.get("/posts/{id}")
async def read_post(id: str):
    validate_uuid(id)
    cursor.execute(""" SELECT * FROM posts WHERE id=%s; """, (id,))
    target_post = cursor.fetchone()
    if not target_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"data": target_post}


@app.delete("/posts/{id}")
async def delete_post(id: str):
    validate_uuid(id)
    cursor.execute(""" DELETE FROM posts WHERE id=%s RETURNING title; """, (id,))
    target_post = cursor.fetchone()
    if not target_post:
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    return {"delete_success": target_post}


@app.put("/posts/{id}")
async def update_post(id: str, post: Post):
    validate_uuid(id)
    cursor.execute(
        """ UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *; """,
        (post.title, post.content, post.published, id),
    )
    update_post = cursor.fetchone()
    if not update_post:
        raise HTTPException(status_code=404, detail="Post not found")
    conn.commit()
    return {"update_success": update_post}
