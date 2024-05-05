from fastapi import FastAPI
from db import models
from routers import blog, user
from db.db import engine


app = FastAPI(description='blog api')

app.include_router(blog.router)
app.include_router(user.router)

# Startup database (magritte)
models.Base.metadata.create_all(engine)


