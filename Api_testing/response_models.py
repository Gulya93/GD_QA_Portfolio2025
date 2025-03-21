from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional


class ApiError(BaseModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str


class CatBreed(BaseModel):
    breed: str
    country: str
    origin: str
    coat: str
    pattern: str


class PageLink(BaseModel):
    url: Optional[HttpUrl]
    label: str
    active: bool

class CatBreedsResponse(BaseModel):
    current_page: int
    data: List[CatBreed]
    first_page_url: HttpUrl
    from_: int = Field(..., alias="from")
    last_page: int
    last_page_url: HttpUrl
    links: List[PageLink]
    next_page_url: Optional[HttpUrl]
    path: HttpUrl
    per_page: int
    prev_page_url: Optional[HttpUrl]
    to: int
    total: int