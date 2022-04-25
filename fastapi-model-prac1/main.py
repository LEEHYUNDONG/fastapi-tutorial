from http.client import HTTPException
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
# from passlib.context import CryptContext
from database import SessionLocal, engine
import model
import schemas
import crud


# pwd_context = CryptContext(schemes=["bcrypt"])
# model connection
model.Base.metadata.create_all(bind=engine)

# app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# template
templates = Jinja2Templates(directory="templates")


# class UserInDB(User):
#     hashed_password: str


# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_passowrd_hash(password):
#     return pwd_context.hash(password)


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def authenticate_user(dummy_db, username: str, password: str):
#     user = get_user(dummy_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/login", response_class=HTMLResponse)
async def login(request:Request):
    return templates.TemplateResponse("index.html", {"request":request})

@app.get("/users/", response_model=schemas.User)
def read_users(skip:int = 0, limit=100, db : Session = Depends(get_db)):
    users = crud.get_user(db, skip=skip, limit=limit)
    return users

@app.post("/users/", response_model=schemas.User)
def create_user(user : schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

# 만약 유저가 존재하지 않는다면 exception error 발생
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
