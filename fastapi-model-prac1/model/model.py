from enum import auto
import typing
from pydantic import BaseModel, Field
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=auto)

class User(BaseModel):
    id : str = Field(..., regex=r'^[a-zA-Z0-9]*@[a-zA-Z]*.com$')
    password : str

class UserInDB(User):
    hashed_password:str

    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_passowrd_hash(password):
    return pwd_context.hash(password)

def get_user(db, username : str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(dummy_db, username:str, password : str):
    user = get_user(dummy_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user




# user = User(id="leerfer@naver.com", password="1234")
# print(user)

# login
# https://fastapi.tiangolo.com/tutorial/security/

# oauth + passlib
# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

# database
# https://fastapi.tiangolo.com/tutorial/sql-databases/ 