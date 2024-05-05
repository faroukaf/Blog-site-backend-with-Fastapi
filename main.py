from fastapi import FastAPI, Depends, status, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from schema import blog, user
from db import models
from routers import blog, user
from db.db import engine, get_db
# from util.hashing import Hash


app = FastAPI(description='blog api')

app.include_router(blog.router)
app.include_router(user.router)

# Startup database (magritte)
models.Base.metadata.create_all(engine)


