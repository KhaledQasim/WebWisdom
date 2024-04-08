# Declare schemas using pydantic, this allows a uniform data , apply validation to our data, and convert between json and python objects
from typing import Annotated, Any
from enum import Enum
from datetime import date
from pydantic.functional_validators import AfterValidator
from fastapi import Query
from urllib.parse import urlparse

from pydantic import (
    Json,
    BaseModel,
    ValidationError,
    ValidationInfo,
    field_validator,
    EmailStr, 
    Field,
    HttpUrl,
    
)

import re



# The common attributes of UserCreate and User class go here to avoid duplication
class UserBase(BaseModel):
    # the "= ..." tells fastapi and pydantic that this is a required field
    username: EmailStr = ...
  


# Code below is a custom validator for password syntax since I could not find a regex that would work for all cases
def check_password_syntax(password: str):
    
    password_regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!£$%^&*_@~#?])[a-zA-Z\d!£$%^&*_@~#?]{8,25}$')
    if password_regex.match(password):
            return True
    else:
            return False


# Password is provided here since this is the only class that will not be returned by our API (we don't want to return the password)
class UserCreate(UserBase):
    # TODO add password regex
    password: str

    @field_validator('password')
    @classmethod
    def check_alphanumeric(cls, v: str):
        if (check_password_syntax(v) == True):
            return v
        else:
            raise ValueError(
                "Password must contain at least one uppercase letter, one lowercase letter, one number and one special character of : !£$%^&*_@~#?")


# Here we are returning data from the database, so we can now include the other attributes e.g id
class User(UserBase):
    id: int
    disabled: bool
    role: str

    class ConfigDict:
        # orm_mode is now deprecated in favor of from_attributes
        # orm_mode = True
        from_attributes = True


class UserInDB(User):
    hashed_password: str





class URL(BaseModel):
    url: HttpUrl
 