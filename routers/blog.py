from fastapi import APIRouter, status, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from schema import blog
from .repository import blog as bg
from db.db import get_db



router = APIRouter(
  prefix='/blog',
  tags=['Blogs']
)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=List[blog.ShowBlog]
)
async def index(
  db: Session = Depends(get_db),
  published: Optional[bool] = False, 
  limit: int = 10,
  sort: Optional[bool] = None
) :
  return await bg.index(
    db, published,
    limit, sort
  )


@router.get(
    '/{blog_id}',
    status_code=status.HTTP_200_OK,
    response_model=blog.ShowBlog
)
def view_blog(
  blog_id: int,
  db: Session = Depends(get_db)
  
):
  return bg.view(blog_id, db)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED
)
def create_blog(
  my_request: blog.Blog,
  db: Session = Depends(get_db)
):
  return bg.create(my_request, db)


@router.delete(
    '/{blog_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_blog(
  blog_id: int,
  db: Session = Depends(get_db)
  
):
  return bg.delete(blog_id, db)



@router.put(
    '/{blog_id}',
    status_code=status.HTTP_202_ACCEPTED
)
def update_blog(
  blog_id: int,
  my_request: blog.Blog,
  db: Session = Depends(get_db)
  
):
  return bg.update(
    blog_id, my_request, db
  )



