from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime, ForeignKey
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime,timezone
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.auth.models import User
    from src.models.books.models import Book

from .schemas import CreateReviews

class Reviews(CreateReviews, table=True):
    __tablename__ = "reviews"
    id: UUID = Field(sa_column=Column("id", pg.UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True))
    created_by: UUID = Field(sa_column=Column("user_id", pg.UUID(as_uuid=True), ForeignKey("users.id"), nullable=False))
    created_at: datetime = Field(
        sa_column=Column("created_at", DateTime(timezone=True), nullable=False,default=lambda: datetime.now(timezone.utc) )
    )
    updated_at: datetime = Field(
        sa_column=Column("updated_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    )
    
    user: Optional["User"] =  Relationship(back_populates="reviews")
    book: Optional["Book"] =  Relationship(back_populates="reviews")
    def __repr__(self):
        return f"<Review(id={self.id}, book_id={self.book_id}, user_id={self.user_id}, rating={self.rating})>"