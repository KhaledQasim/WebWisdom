from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    disabled = Column(Boolean, default=False)
    hashed_password = Column(String)
    role = Column(String, default="user")
    
    # Add a relationship to Results
    results = relationship("Results", back_populates="user")

    
class Results(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, index=True)
    result = Column(Text, nullable=False)  # Long text field
    user_id = Column(Integer, ForeignKey('users.id'))  # Foreign key to users table
    created_at = Column(DateTime(timezone=True), default=func.now())  # Auto-set to current time
    # Relationship to link back to the Users model
    user = relationship("Users", back_populates="results")
   