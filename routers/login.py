import sys
sys.path.append("..")
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from db.models import User
from schema import login as l, user
from util.hashing import Hash



router = APIRouter(
  # prefix='/',
  tags=['Auth']
)


@router.post(
  '/login',
  response_model=user.ShowUser,
  status_code=status.HTTP_202_ACCEPTED
)
def login(
  request: l.Login,
  db: Session = Depends(get_db)
):
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

  return user



