
from datetime import datetime
import email
from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from app1.database import Base

class PostBase(BaseModel):
    title:str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email:EmailStr 

    class Config:
        orm_mode = True
        
class Post(PostBase):  
    id: int
    created_at : datetime
    onwer_id: int
    owner: UserOut
    class Config:
        orm_mode = True
  


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)