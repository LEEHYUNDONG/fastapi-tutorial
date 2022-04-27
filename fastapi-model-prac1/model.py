from enum import auto
import typing
from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30))
    fullname = Column(String(30), nullable=True)
    password = Column(String(200))



    # user = User(id="leerfer@naver.com", password="1234")
    # print(user)

    # login
    # https://fastapi.tiangolo.com/tutorial/security/

    # oauth + passlib
    # https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

    # database
    # https://fastapi.tiangolo.com/tutorial/sql-databases/
