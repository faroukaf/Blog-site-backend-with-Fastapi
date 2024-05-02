from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI(description='blog api')

class Blog(BaseModel):
  title: str
  body: str
  published: Optional[bool]

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
def create_blog(request: Blog):
  return {
    'data': 'blog created'
  }


