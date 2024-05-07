import sys
sys.path.append("..")
from datetime import timedelta
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schema import login as l, user
from db.db import get_db
from db.models import User
from schema.token import Token
from util.hashing import Hash
from util.JWToken import create_access_token
from util.oauth2 import get_current_user



router = APIRouter(
  # prefix='/',
  tags=['Auth']
)


ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post(
  '/login',
  # response_model=None,#Token,#dict[str, str],
  # status_code=status.HTTP_202_ACCEPTED
)
def login(
  request: OAuth2PasswordRequestForm = Depends(),
  db: Session = Depends(get_db)
) -> dict[str, str]:
  user = db.query(User).filter(User.email == request.username).first()

  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'No user with email {request.username}'
    )

  if not Hash.verify(user.password, request.password):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'Wrong password'
    )

  access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    {'sub': request.username},
    access_token_expire
  )
  # return {'access_token': access_token, 'type': 'bearer'}
  return Token(access_token=access_token, token_type='bearer').model_dump()


@router.get(
  '/me',
  status_code=status.HTTP_200_OK
)
def get_user(
  current_user: user.User = Depends(get_current_user)
):
  return current_user



