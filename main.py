from fastapi import FastAPI
from db import models
from routers import blog, user, login
from db.db import engine


app = FastAPI(description='blog api')

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(login.router)

# Startup database (magritte)
models.Base.metadata.create_all(engine)


