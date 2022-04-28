# Base
from fastapi import Depends, FastAPI, Form, Request, Response
from pydantic import BaseModel, Field
from typing import Optional
from datetime import timedelta

# templates
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# login, password, key
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from os import urandom
from fastapi_login import LoginManager
from requests import RequestException
from fastapi_login.exceptions import InvalidCredentialsException

# Response
from starlette.responses import RedirectResponse, HTMLResponse


# DB
from DB import DB

"""
sql alchemy 사용하지 않고,
dummy_db를 이용하여 template으로 로그인, 회원가입, 로그인 화면을 따로 
redirection까지 구현하기
"""

app = FastAPI()


"""SECRET KEY 생성"""
SECRET_KEY = urandom(30).hex()

"""for hashing password by one way"""
pwd_ctx = CryptContext(schemes=["bcrypt"])

"""Login Manager"""
managers = LoginManager(secret=SECRET_KEY, token_url='/login', use_cookie=True)

# template
templates = Jinja2Templates(directory="templates")
"""static mount"""
app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/templates", Jinja2Templates(directory="templates"), name="templates")


"""
user model 과 실제 db 테이블에 적재될 정보 포함된 userdb
User : user in
UserDB : user out
"""

class User(BaseModel):
    username : str
    fullname : Optional[str]
    password : Optional[str]
    age : Optional[int]

class UserInDB(User):
    hashed_password : str


"""save user in db"""
def save_user(user_in:User):
    hashed_password = get_hashed_password(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    return user_in_db

def get_user(username : str, db):
    if username in db.keys():
        user = db.get(username)
        return UserInDB(**user) # 일반 dictionary call에 비해 오류 발생 용이
        

"""
password hashing
param
plain_password : user's password
"""
def get_hashed_password(plain_password):
    return pwd_ctx.hash(plain_password)

"""
verifying the password
plain_password : user's input pwd
hashed_password : the user's hashed pwd
"""
def verify_password(plain_password, hashed_password):
    return pwd_ctx.verify(plain_password, hashed_password)

def authenticate_user(username : str, password : str, db):
    user = get_user(username, db).dict()
    if not user:
        return False
    if not verify_password(password, user.get("hashed_password")):
        return False
    return user


""" use fake db getting user db"""
fake_db = DB.get("users")

"""test password"""
# password = "1234"
# print(pwd_ctx.hash(password))

"""test"""
# fake_user = User(username="hyundong", password="password")
# fake_user_db = save_user(fake_user)
# print(get_user(username=fake_user.username, db=fake_db))
# print(authenticate_user(username="hyundong", password='password', db=fake_db))


@managers.user_loader()
def load_user(username:str, db):
    user = get_user(username, db)
    return user

"""index"""
@app.get("/index", response_class=HTMLResponse)
def index(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})


"""login"""
@app.get('/login', response_class=HTMLResponse)
async def login(request:Request):
    return templates.TemplateResponse("login.html", {"request":request})


@app.post('/login')
def login(response:Response, data:OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):
    username = data.username
    password = data.password
    user = load_user(username, fake_db)
    # resp = Response.set_cookie(key="")
    if not user:
        raise InvalidCredentialsException
    elif not verify_password(password, user.hashed_password):
        raise InvalidCredentialsException

    """create access token"""
    access_token = managers.create_access_token(
        data=dict(sub=username), expires=timedelta(hours=12)
    )
    print(access_token)
    """set cookie"""
    managers.set_cookie(response, access_token)
    return RedirectResponse(url='/index', status_code=302)
    


"""register"""
@app.get('/signup', response_class=HTMLResponse)
async def signup(request:Request):
    return templates.TemplateResponse("signup.html", {"request":request})

@app.post('/signup')
async def signup(request : Request, response: Response):
    tmp = await request.form()
    user = tmp._dict
    print(user)
    new_user = User(username=user.get("username"), fullname=user.get("fullname"), age=user.get("age"), password=user.get("password"))
    # new_user = User(user)
    
    """data 저장하는거 해보기"""
    fake_user_db = save_user(new_user)
    fake_db[new_user.username] = fake_user_db
    if new_user:
        return RedirectResponse(url='/login', status_code=302)

#  Exception in ASGI application