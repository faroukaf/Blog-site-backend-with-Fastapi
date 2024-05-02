from fastapi import FastAPI, Depends
from typing import Optional
from sqlalchemy.orm import Session
from schema import blog
from db import models
from db.db import engine, get_db


app = FastAPI(description='blog api')

# Startup database (magritte)
models.Base.metadata.create_all(engine)


@app.get('/blog')
def index(
  published: bool, 
  limit: int = 10,
  sort: Optional[bool] = None
):
  if published:
    return {
      'data': f'{limit} blog list published'
    }

  else:
    return {
      'data': f'{limit} blog list un/published'
    }


@app.get('/blog/unpublished')
def unpublished():
  return 'jk'

@app.get('/blog/{blog_id}')
def view_blog(blog_id: int) -> dict:
  return {
    'data': blog_id
  }

@app.get('/blog/{blog_id}/comments')
def view_blog_comments(blog_id: int) -> dict:
  return {
    'data': [1, 2]
  }

@app.post('/blog')
def create_blog(
  my_request: blog.Blog,
  db: Session = Depends(get_db)
):
  blog = models.Blog(
    title = my_request.title,
    body = my_request.body,
  )

  db.add(blog)
  db.commit()
  db.refresh(blog)

  return {'data': blog}


