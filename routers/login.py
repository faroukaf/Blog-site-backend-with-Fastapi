import sys
sys.path.append("..")
from datetime import timedelta
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from db.models import User
from schema import login as l, user
from util.hashing import Hash
from util.JWToken import create_access_token



router = APIRouter(
  # prefix='/',
  tags=['Auth']
)


ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post(
  '/login',
  response_model=dict[str, str],
  status_code=status.HTTP_202_ACCEPTED
)
def login(
  request: l.Login,
  db: Session = Depends(get_db)
) -> dict[str, str]:
  user = db.query(User).filter(User.email == request.email).first()

  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'No user with email {request.email}'
    )

  if not Hash.verify(user.password, request.password):
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'Wrong password'
    )

  access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    {'sub': request.email},
    access_token_expire
  )
  return {'access_token': access_token, 'type': 'bearer'}



