from pydantic import BaseModel
from typing import List


class Blog(BaseModel):
    title: str
    body: str


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog] = []


class ShowBlog(Blog):
    title: str
    body: str
    creator: ShowUser


class Login(BaseModel):
    username: str
    password: str

