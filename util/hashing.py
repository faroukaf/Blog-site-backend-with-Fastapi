from passlib.context import CryptContext



pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated='auto')


class Hash():
  def bcrypt(password: str) -> str:
    return pwd_cxt.hash(password)

  def verify(hashed: str, plain: str) -> bool:
    return pwd_cxt.verify(plain, hashed)


