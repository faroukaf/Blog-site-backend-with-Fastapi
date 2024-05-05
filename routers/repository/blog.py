import sys
sys.path.append("...")
from fastapi import Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from schema import blog
from db import models
from db.db import get_db



async def index(
  published: Optional[bool] = False, 
  limit: int = 10,
  sort: Optional[bool] = None,
  db: Session = Depends(get_db)
) :
  if published:
    blogs = db.query(models.Blog).\
      filter(models.Blog.published == True)\
        .limit(limit).all()
    return blogs

  else:
    blogs = db.query(models.Blog).limit(limit).all()
    return blogs


def view(
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


def create(
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


def delete(
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


def update(
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



