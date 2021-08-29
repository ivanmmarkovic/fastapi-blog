from typing import List, Optional
from pydantic import BaseModel
from pydantic.types import SecretStr


class Article(BaseModel):
    title: str
    body: str

class User(BaseModel):
    name: str
    email: str
    password: str


class ArticleSchemaResponse(BaseModel):
    id: int
    title: str
    body: str
    user_id: int

    class Config():
        orm_mode = True

class UserSchemaResponse(BaseModel):
    id: int
    name: str
    email: str
    articles: List[ArticleSchemaResponse]

    class Config():
        orm_mode = True



