from sqlalchemy.orm import Session

from . import models, schemas
# All the sql database queries are resilient to sql injection attacks since  we are using an orm (sqlalchemy) to interact with the database

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()
    
def get_user_by_username(db: Session, username: str):
    return db.query(models.Users).filter(models.Users.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Users).offset(skip).limit(limit).all()

def create_user(db: Session, userModel: models.Users):
    db.add(userModel)
    db.commit()
    db.refresh(userModel)






# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Form).offset(skip).limit(limit).all()