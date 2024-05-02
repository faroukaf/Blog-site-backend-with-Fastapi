from sqlalchemy import Column, Integer, String, Boolean
from .db import Base



class Blog(Base):
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String)
  body = Column(String)
  published = Column(Boolean)




