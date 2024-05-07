import sys
sys.path.append("...")
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schema import user
from db import models
from util.hashing import Hash



def create(
  my_request: user.User,
  db: Session
):
  inp = my_request.model_dump()
  inp['password'] = Hash.bcrypt(inp['password'])
  new_user = models.User(**inp)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


def show(
  user_id: str,
  db: Session
):
  user = db.query(models.User).filter(models.User.id == user_id).first()
  if not user:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with id {user_id} not exist'
    )

  return user



