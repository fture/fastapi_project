from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.params import Body
from uuid import uuid4, UUID


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str = None


my_posts = [
    {"title": "title1", "content": "content1", "id": uuid4()},
    {"title": "title2", "content": "content2", "id": uuid4()},
]


def find_post(id: str):
    for i in my_posts:
        if i["id"] == id:
            return i


@app.get("/")
async def read_root():
    return {"data": "Post"}


@app.get("/posts")
async def read_post():
    return {"data": my_posts}


@app.post("/posts")
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = uuid4()

    my_posts.append(post_dict)
    return {"post": post_dict}


@app.get("/posts/{id}")
async def read_post_by_id(id: UUID):
    post = find_post(id)
    return {"post": post}
