from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, String, DateTime
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.books.models import Book
    from src.models.reviews.models import Reviews

from .schemas import BaseUser

class User(BaseUser, table=True):
    __tablename__ = "users"
    
    id: UUID = Field(sa_column=Column("id", pg.UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True))
    is_verified: bool = Field(
        default=False,
        sa_column=Column(pg.BOOLEAN, default=False, nullable=False)
    )
    role: str = Field(
        sa_column=Column(String(20), nullable=False, server_default="user")
    )
    hashed_password: str = Field(
        sa_column=Column(String(255), nullable=False), exclude=True
    )
    books: List["Book"] =  Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})
    reviews: List["Reviews"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})
    created_at: datetime = Field(
        default=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime, default=datetime.now, nullable=False)
    )
    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime, onupdate=datetime.now)
    )
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"