from typing import List
from pydantic import BaseModel


class ShowUser2Blog(BaseModel):
  name: str
  class Config:
    orm_mode = True


