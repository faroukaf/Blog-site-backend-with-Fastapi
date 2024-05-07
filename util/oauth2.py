from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from util import JWToken



oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
  credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'}
  )

  return JWToken.verify_token(
    token, credential_exception
  )
  # user = get_user(db, username=token_data.username)
  # if user is None:
  #   raise credential_exception
  # return user


