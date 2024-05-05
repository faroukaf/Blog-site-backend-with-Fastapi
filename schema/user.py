from typing import List
from pydantic import BaseModel
from .blog import ShowBlog2User


class User(BaseModel):
  name: str
  email: str
  password: str

class ShowUser(BaseModel):
  name: str
  email: str
  blogs: List[ShowBlog2User]

  class Config:
    orm_mode = True


