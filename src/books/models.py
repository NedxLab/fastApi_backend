from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, String, DateTime
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime,timezone
from typing import Optional

class BookCreate(SQLModel):
    title: str = Field(sa_column=Column("title", String, nullable=False))
    author: str = Field(sa_column=Column("author", String, nullable=False))
    pages: int = Field(sa_column=Column("pages", Integer, nullable=False))
    summary: str = Field(sa_column=Column("summary", String, nullable=True))
    isbn: str = Field(sa_column=Column("isbn", String, nullable=False, unique=True))
    publisher: str = Field(sa_column=Column("publisher", String, nullable=True))
    year: int = Field(sa_column=Column("year", Integer, nullable=True))
    genre: str = Field(sa_column=Column("genre", String, nullable=True))
    created_by: Optional[UUID] = Field(sa_column=Column("created_by", pg.UUID(as_uuid=True), nullable=True, default=None, foreign_key="users.id"))

class Book(BookCreate, table=True):
    id: UUID = Field(sa_column=Column("id", pg.UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True))
    created_at: datetime = Field(
        sa_column=Column("created_at", DateTime(timezone=True), nullable=False,default=lambda: datetime.now(timezone.utc) )
    )
    updated_at: datetime = Field(
        sa_column=Column("updated_at", DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    )
    
    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author}, isbn={self.isbn})>"

class BookResponse(SQLModel):
    book: Book

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