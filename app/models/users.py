from sqlalchemy import Column, String, Integer
from config import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    user = Column(String, unique=True)
    password = Column(String)
