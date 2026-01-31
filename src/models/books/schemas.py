from uuid import UUID
from datetime import datetime
from typing import Optional,List
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, String
from src.models.auth.schemas import UserBasicResponse

class BookCreate(SQLModel):
    title: str = Field(sa_column=Column("title", String, nullable=False))
    author: str = Field(sa_column=Column("author", String, nullable=False))
    pages: int = Field(sa_column=Column("pages", Integer, nullable=False))
    summary: str = Field(sa_column=Column("summary", String, nullable=True))
    isbn: str = Field(sa_column=Column("isbn", String, nullable=False, unique=True))
    publisher: str = Field(sa_column=Column("publisher", String, nullable=True))
    year: int = Field(sa_column=Column("year", Integer, nullable=True))
    genre: str = Field(sa_column=Column("genre", String, nullable=True))
 
class BookBasicResponse(BookCreate):
    id: UUID
    created_at: datetime 

class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    pages: Optional[int] = None
    summary: Optional[str] = None
    isbn: Optional[str] = None  
    publisher: Optional[str] = None
    year: Optional[int] = None
    genre: Optional[str] = None
    
    model_config = {"extra": "forbid"}


from src.models.reviews.schemas import ReviewBasicResponse
class BookResponse(BookCreate):
    id: UUID
    created_at: datetime
    user: Optional[UserBasicResponse] = None  
    reviews: List[ReviewBasicResponse] = None  