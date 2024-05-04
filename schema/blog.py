from typing import Optional
from pydantic import BaseModel
from .user import ShowUser


class Blog(BaseModel):
  title: str
  body: str
  published: Optional[bool]


class ShowBlog(BaseModel):
  title: str
  body: str
  published: Optional[bool]
  author: ShowUser
  class Config:
    orm_mode = True
