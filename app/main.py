from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from .database import Base, engine
from .config import settings

from .routers import post, user, auth, vote


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
