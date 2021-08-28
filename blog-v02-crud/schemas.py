from typing import Optional
from pydantic import BaseModel
from pydantic.types import SecretStr


class Article(BaseModel):
    title: str
    body: str

