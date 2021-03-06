from pydantic import BaseModel
from typing import List, Optional, Dict


class UserBase(BaseModel):
    username :str
    address : Optional[str] = None
    phone : Optional[str] = None

class UserIn(UserBase):
    pass

class UserDB(UserBase):
    hashed_password : str