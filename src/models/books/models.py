from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, DateTime
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime,timezone
from typing import List, Optional, TYPE_CHECKING
from src.models.auth.models import  User

if TYPE_CHECKING:
    from src.models.reviews.models import Reviews

from .schemas import BookCreate

class Book(BookCreate, table=True):
    __tablename__ = "books"
    id: UUID = Field(sa_column=Column("id", pg.UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True))
    created_at: datetime = Field(
        sa_column=Column("created_at", DateTime(timezone=True), nullable=False,default=lambda: datetime.now(timezone.utc) )
    )
    created_by: Optional[UUID] = Field(
    default=None,
    foreign_key="users.id",
    nullable=True
    )
    updated_at: datetime = Field(
        sa_column=Column("updated_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    )
    user: Optional["User"] =  Relationship(back_populates="books")
    reviews: List["Reviews"] = Relationship(back_populates="book", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})
    
    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author}, isbn={self.isbn})>"