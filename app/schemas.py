
from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostCreate(BaseModel):   #the pydantic scheme helps in valiation and stuffs
    title: str
    content: str
    published: bool = True



class postResponse(BaseModel):
    title:str
    content:str
    published:bool
    created_at:datetime

    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email:EmailStr
    password: str

    print("sex")


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
 
    
    class Config:
        orm_mode = True

class userLogin(BaseModel):
    email: EmailStr
    password: str


    print("noooo")


class token(BaseModel):
    access_token: str
    token_type: str


class tokendata(BaseModel):  #the data that we embed in our access token
    user_id: int