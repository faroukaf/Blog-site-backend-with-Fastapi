import importlib
from typing import Optional
from pydantic import BaseModel
from .show_user_to_blog import ShowUser2Blog


class Blog(BaseModel):
  title: str
  body: str
  published: Optional[bool]


class ShowBlog(BaseModel):
  # user = importlib.import_module('user', package='.')
  title: str
  body: str
  published: Optional[bool]
  author: ShowUser2Blog
  class Config:
    orm_mode = True



class ShowBlog2User(BaseModel):
  title: str
  body: str
  published: Optional[bool]
  class Config:
    orm_mode = True


