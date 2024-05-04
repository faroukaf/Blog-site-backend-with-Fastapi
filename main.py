from fastapi import FastAPI, Depends, status, HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session
from schema import blog, user
from db import models
from db.db import engine, get_db
from util.hashing import Hash


app = FastAPI(description='blog api')

# Startup database (magritte)
models.Base.metadata.create_all(engine)


@app.get(
    '/blog',
    status_code=status.HTTP_200_OK,
    response_model=List[blog.BlogModel],
    tags=['Blogs']
)
async def index(
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


@app.get(
    '/blog/{blog_id}',
    status_code=status.HTTP_200_OK,
    response_model=blog.BlogModel,
    tags=['Blogs']
)
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


@app.post(
    '/blog',
    status_code=status.HTTP_201_CREATED,
    tags=['Blogs']
)
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


@app.delete(
    '/blog/{blog_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Blogs']
)
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



@app.put(
    '/blog/{blog_id}',
    status_code=status.HTTP_202_ACCEPTED,
    tags=['Blogs']
)
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



@app.post(
  '/user',
  status_code=status.HTTP_201_CREATED,
  response_model=user.ShowUser,
  tags=['Users']
)
def create_user(
  my_request: user.User,
  db: Session = Depends(get_db)
):
  inp = my_request.model_dump()
  inp['password'] = Hash.bcrypt(inp['password'])
  new_user = models.User(**inp)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

@app.get(
  '/user/{user_id}',
  status_code=status.HTTP_200_OK,
  response_model=user.ShowUser,
  tags=['Users']
)
def show_user(
  user_id: str,
  db: Session = Depends(get_db)
):
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with id {user_id} not exist'
    )

  return user



