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


def create_user_test_result(db: Session, result: schemas.Result, user_id: int):
    db_item = models.Results(result=result, user_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)


def get_results_by_id_of_user(db: Session, user_id: int):
    skip = 0
    limit = 100
    return db.query(models.Results).filter(models.Results.user_id == user_id).order_by(models.Results.created_at.desc()).offset(skip).limit(limit).all()


def get_latest_user_result(db: Session,user_id: int):
    return db.query(models.Results).filter(models.Results.user_id == user_id).order_by(models.Results.created_at.desc()).first()


def get_result_by_id(db: Session,id: int):
    return db.query(models.Results).filter(models.Results.id == id).first()



# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Form).offset(skip).limit(limit).all()


# **result.model_dump()