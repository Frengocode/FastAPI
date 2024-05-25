from pydantic import BaseModel
from typing import Optional

class ShowUser(BaseModel):
    name: str
    email: str
    id: int



class Blog(BaseModel):
    title: str
    body: str
    creator_name: str

class ShowBlog(BaseModel):
    title: str
    body: str





class User(BaseModel):
    name: str
    email: str
    password: str
    



class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    accses_token: str
    token_type: str


class TokenData(BaseModel):
    name: Optional[str] = None
