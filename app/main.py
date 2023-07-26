from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from passlib.context import CryptContext
from psycopg2.extras import RealDictCursor
import time
from typing import List
from sqlalchemy.orm import Session
# from sqlalchemy import update, delete
from . import models, schemas, utils
from .database import engine, get_db
from .router import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
