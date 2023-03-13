from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from .database import Base, get_db, engine


from .routers import post, user, auth

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
