from fastapi import FastAPI, Depends, status, HTTPException
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
  published: Optional[bool] = False, 
  limit: int = 10,
  sort: Optional[bool] = None,
  db: Session = Depends(get_db)
) :
  blogs = db.query(models.Blog).all()
  if published:
    return {
      'data': f'{limit} blog list published'
    }

  else:
    # return {
    #   'data': [blogs, str(type(blogs)), str(type(blogs[0]))]
    # }
    return blogs


@app.get('/blog/unpublished')
def unpublished():
  return 'jk'

@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK)
def view_blog(
  blog_id: int,
  db: Session = Depends(get_db)
  
):
  blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()

  if not blog:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'Blog with id {blog_id} not exist'
    )

  return blog

@app.get('/blog/{blog_id}/comments')
def view_blog_comments(blog_id: int) -> dict:
  return {
    'data': [1, 2]
  }

@app.post('/blog', status_code=status.HTTP_201_CREATED)
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

  return blog


@app.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(
  blog_id: int,
  db: Session = Depends(get_db)
  
):
  blog = db.query(models.Blog).filter(models.Blog.id == blog_id)

  if not blog.first():
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'Blog with id {blog_id} not exist'
    )
  
  blog.delete(synchronize_session=False)
  db.commit()
  return {
    'detail': 'Blog with id {blog_id} Deleted'
  }



@app.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(
  blog_id: int,
  my_request: blog.Blog,
  db: Session = Depends(get_db)
  
):
  blog = db.query(models.Blog).filter(models.Blog.id == blog_id)

  if not blog.first():
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'Blog with id {blog_id} not exist'
    )

  blog.update(my_request.model_dump())
  db.commit()
  blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
  return blog


