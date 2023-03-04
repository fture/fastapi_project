from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str = ""


@app.get("/")
async def read_root():
    return {"data": Post}


@app.post("/posts")
async def create_post(post: Post):
    print(post)
    return {"post": post}
