from pydantic import BaseModel
from typing import Optional



class Token(BaseModel):
  access_token: str
  token_type: str


class TokenDate(BaseException):
  username: Optional[str] = None


