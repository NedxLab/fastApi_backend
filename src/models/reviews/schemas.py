from uuid import UUID
from datetime import datetime 
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, String, ForeignKey
import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from src.models.auth.schemas import UserBasicResponse
 
class BookInfo(SQLModel):
    id: UUID
    title: str
    author: str
    isbn: str
    
    model_config = {"from_attributes": True}

class CreateReviews(SQLModel):
    review: str = Field(sa_column=Column("review", String, nullable=False))
    rating: int = Field(sa_column=Column("rating", Integer, nullable=False))
    book_id: UUID = Field(sa_column=Column("book_id", pg.UUID(as_uuid=True), ForeignKey("books.id"), nullable=False))
class ReviewBasicResponse(CreateReviews):
    id: UUID
    created_at: datetime
    updated_at: datetime 
    

from src.models.books.schemas import BookBasicResponse
class ReviewResponse(CreateReviews):
    id: UUID
    created_at: datetime
    updated_at: datetime
    user: Optional[UserBasicResponse] = None 
    book: Optional[BookBasicResponse] = None 
