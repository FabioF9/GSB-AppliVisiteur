from typing import List
from pydantic import BaseModel

class BlogBase(BaseModel):
    title:str
    body:str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUserBlogs(BaseModel):
    name:str
    email:str

class ShowUser(BaseModel):
    name:str
    email:str 
    blogs:List[Blog] = []
    class Config():
        orm_mode = True
    

class ShowBlog(BaseModel):
    title: str
    body:str
    creator: ShowUserBlogs

    class Config():
        orm_mode = True

class Medecin(BaseModel):
    nom : str
    spe : str
    ville : str


class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None