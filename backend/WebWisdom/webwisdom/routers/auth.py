from typing import Annotated
from datetime import datetime, timedelta , timezone
from fastapi import Depends, APIRouter, HTTPException, status, Cookie, FastAPI , Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlalchemy.orm import Session


from ..database.database import SessionLocal , engine

from ..database import models, schemas, crud

from ..config.config import Config




router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    # dependencies=[Depends(oauth2_scheme)],

)

SECRET_KEY = Config.SECRET_KEY
ALGORITHM = Config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = int(Config.ACCESS_TOKEN_EXPIRE_MINUTES)


argon2_context = CryptContext(schemes=['argon2'], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Dependency needed to be used in every file that needs to access the database, below when using "yield" it will create new SQLAlchemy SessionLocal for a single request and then close it once the request is finished.


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependancy = Annotated[Session, Depends(get_db)]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None



def verify_password(plain_password, hashed_password):
    return argon2_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return argon2_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(db : db_dependancy ,jwt_token: Annotated[str , Cookie() ]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        
        payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user




@router.post("/register")
async def register_new_user(
    db: db_dependancy,
    create_user_request: schemas.UserCreate
):
    request_username = crud.get_user_by_username(db, create_user_request.username)
    if request_username is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already in use"
        )
        
   
    
    create_user_model = models.Users(
        username = create_user_request.username,
        hashed_password = argon2_context.hash(create_user_request.password),
        disabled = False
    )
    
    crud.create_user(db, create_user_model)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": create_user_request.username, "grant_type": "access"}, expires_delta=access_token_expires
    )
    
  
    content = {"message": "Account Created Successfully"}
    response = JSONResponse(content=content)
    response.set_cookie(key="jwt_token", value=access_token, expires=(int(Config.ACCESS_TOKEN_EXPIRE_MINUTES)*60) , secure=True , httponly=True, samesite="lax")
    return response
    

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db : db_dependancy
) :
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "grant_type": "access"}, expires_delta=access_token_expires
    )
    # return Token(access_token=access_token, token_type="bearer")
    content = {"message": "Login Successful"}
    response = JSONResponse(content=content)
    response.set_cookie(key="jwt_token", value=access_token, expires=(int(Config.ACCESS_TOKEN_EXPIRE_MINUTES)*60) , secure=True , httponly=True, samesite="lax")
    return response




# Validate jwt token then return current user and their properties 
# @router.get("/users/me/", response_model=schemas.User)
# async def read_users_me(
#     current_user: Annotated[schemas.User, Depends(get_current_active_user)]
# ):
#     return current_user



# Validate jwt token inside the jwt cookie then return current user and their properties and update the jwt expired time
@router.get("/users/me-cookie/", response_model=schemas.User)
async def read_users_me(
    user: Annotated[schemas.User, Depends(get_current_active_user)],  
):
    return user



@router.get("/logout")
async def logout():
    content = {"message": "Logout Successful"}
    response = JSONResponse(content=content)
    response.set_cookie(key="jwt_token", value="", expires=(int(Config.ACCESS_TOKEN_EXPIRE_MINUTES)*60) , secure=True , httponly=True, samesite="lax")
    return response 

       


# @router.get("/users/me-cookie/")
# def read_users_me(
#     jwt: str | None = Cookie(default=None)
# ):
#     return {"jwt":jwt}
# @router.get("/users/me-cookie/")
# def read_users_me(
#     jwt: Annotated[str , Cookie() ] 
# ):
#     return {"jwt":jwt}
