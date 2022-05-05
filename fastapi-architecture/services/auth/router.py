from multiprocessing import managers
from fastapi import APIRouter, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from services.auth.utility import authenticate_user
from utility import authenticate_user, manager

endpoint = APIRouter(
    prefix="/login",
    tags = ["login"]
)

"""
패키지 관점, 권한 관점에서 router를 분리해야 한다.
"""

@endpoint.get('')
def login_get():
    return {"hello world":"Fast API"}


@endpoint.post('')
def login_post(user : OAuth2PasswordRequestForm = Depends()):
    if authenticate_user(user.username, user.password):
        token = managers.create_access_token(data = {"sub":user.username})
        resp = RedirectResponse('/', status_code=302)
        manager.set_cookie(resp, token)
        return resp
    else:
        return RedirectResponse('login', status_code=307)

@endpoint.get('/test')
def login_test(user = Depends(manager)):
    return {"Yo" : "Login Success1"}
