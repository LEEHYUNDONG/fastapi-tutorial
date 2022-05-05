import sys,os
from os import path
base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(base_dir)
from lib2to3.pgen2 import token
from fastapi_login import LoginManager
from passlib.context import CryptContext
from core.models.database import users
from core.schemas.user import UserOut
from fastapi.response import RedirectResponse
from fastapi import Request


pass_ctx = CryptContext(schemes=["bcrypt"])

def get_hashed_password(plain_password):
    return pass_ctx.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return pass_ctx.verify(plain_password, hashed_password)

def authenticate_user(username:str, password : str):
    if username in users:
        return verify_password(password, users[username].get("hashed_password"))

# print(get_hashed_password("passoword"))

class NotAuthenticatedException(Exception):
    pass

manager = LoginManager(
    os.urandom(24).hex(),
    token_url="/login",
    use_cookie= True,
    custom_exception = NotAuthenticatedException
)



@manager.user_loader()
def user_loader(username):
    if username in users:
        return UserOut(**users[username])

def not_authenticated_exception_handler(req : Request, exce : Exception):
    return RedirectResponse('/login')
