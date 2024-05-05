import sys
sys.path.append("..")
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schema import user
from db.db import get_db
from .repository import user as ur



router = APIRouter(
  prefix='/user',
  tags=['Users']
)


@router.post(
  '/',
  status_code=status.HTTP_201_CREATED,
  response_model=user.ShowUser
)
def create_user(
  my_request: user.User,
  db: Session = Depends(get_db)
):
  return ur.create(my_request, db)

@router.get(
  '/{user_id}',
  status_code=status.HTTP_200_OK,
  response_model=user.ShowUser
)
def show_user(
  user_id: str,
  db: Session = Depends(get_db)
):
  return ur.show(user_id, db)



