from typing import Optional
from jose import jwt
from datetime import timedelta, datetime



SECRET_KEY = \
  '8d5823a54274ade03dfa1358d5e068ca61d178fd56532423051db796b0d0b476'
ALGORISM = 'HS256'


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)

  to_encode.update({'exp': expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORISM)
  return encoded_jwt



