import sys
sys.path.append("..")
from fastapi import APIRouter, status
from schema import user
from util.hashing import Hash



router = APIRouter(
  # prefix='/',
  tags=['Auth']
)


@router.post(
  '/login',
  # response_model=
  status_code=status.HTTP_202_ACCEPTED
)
def login(
  re
):
  return 'login'



