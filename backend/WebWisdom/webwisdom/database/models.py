from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)
    role = Column(String, default="user")
    
