from typing import Optional
from pydantic import BaseModel


class Blog(BaseModel):
  title: str
  body: str
  published: Optional[bool]


class ShowBlog(Blog):
  class Config:
    orm_mode = True
