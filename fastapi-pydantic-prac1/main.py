from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext


app = FastAPI()
pass_ctx = CryptContext(schemes=["bcrypt"], ) # scheme
template = Jinja2Templates(directory = "templates")
# templates.TemplateResponse("index.html", {"name":"g"})
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_hashed_password(plain_password:str):
    return pass_ctx.hash(plain_password)

def verify_password(plain_password:str, hashed_password:str): 
    return pass_ctx.verify(plain_password, hashed_password)

@app.get('/{id}')
def index(id:int):
    return {"hell":id}
# template request를 왜 객체랑 함께 보내야 하는가 ?

# print(get_hashed_password("mypass"))
# print(verify_password("password", get_hashed_password("password")))