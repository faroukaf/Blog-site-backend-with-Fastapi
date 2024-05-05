import sys
sys.path.append("..")
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from sqlalchemy.orm import Session
from schema import user
from db import models
from db.db import get_db
from util.hashing import Hash



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
  inp = my_request.model_dump()
  inp['password'] = Hash.bcrypt(inp['password'])
  new_user = models.User(**inp)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

@router.get(
  '/{user_id}',
  status_code=status.HTTP_200_OK,
  response_model=user.ShowUser
)
def show_user(
  user_id: str,
  db: Session = Depends(get_db)
):
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with id {user_id} not exist'
    )

  return user



