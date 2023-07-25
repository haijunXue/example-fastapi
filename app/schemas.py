from pydantic import BaseModel, EmailStr, config
from typing import Optional
from datetime import datetime
from pydantic.types import conint
from . import models

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    owner_id: int
    
    
class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    
    
    class Config:
        orm_mode = True
        
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class Post(BaseModel):
    id: int
    created_at: datetime
    owner_id: int
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
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None
    
    
class PostOut(BaseModel):
    id: int
    created_at: datetime
    
  
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
    