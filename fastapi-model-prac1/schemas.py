from pydantic import BaseModel, Field
from fastapi import FastAPI


class UserBase(BaseModel):
    email:str

class UserCreate(UserBase):
    password : str
        
class User(UserBase):
    id: int
    email: str = Field(..., regex=r'^[a-zA-Z0-9]*@[a-zA-Z]*.com$')
    # fullname: str = Field(..., regex=r'^[a-zA-Z]$')
    password: str

    class Config:
        orm_mode = True