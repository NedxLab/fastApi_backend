from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import Column, Integer, String, DateTime
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime, timezone
from typing import List, Optional, TYPE_CHECKING
from pydantic import   model_validator

if TYPE_CHECKING:
    from src.models.books import models

 

class BaseUser(SQLModel):
    username: str = Field(
        sa_column=Column(String(50), unique=True, nullable=False)
    )
    first_name: str = Field(
        sa_column=Column(String(50), nullable=False)
    )
    last_name: str = Field(
        sa_column=Column(String(50), nullable=False)
    )
    role: str = Field(
        sa_column=Column(String(20), nullable=False, server_default="user")
    )
    
    email: str = Field(
        sa_column=Column(String(100), unique=True, nullable=False)
    )
class CreateUser(BaseUser):
    password: str = Field(
        sa_column=Column(String(255), nullable=False),  exclude=True
    )

class User(BaseUser, table=True):
    __tablename__ = "users"
    
    id: UUID = Field(sa_column=Column("id", pg.UUID(as_uuid=True), nullable=False, default=uuid4, primary_key=True))
    is_verified: bool = Field(
        default=False,
        sa_column=Column(pg.BOOLEAN, default=False, nullable=False)
    )
    hashed_password: str = Field(
        sa_column=Column(String(255), nullable=False), exclude=True
    )
    books: List["Book"] =  Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"})
   
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
    
class LoginUser(SQLModel):
    username: str | None = Field(None, max_length=50)
    email: str | None = Field(None, max_length=100)
    password: str = Field(..., min_length=8)
    
    @model_validator(mode='after')
    def check_identifier(self):
        if not self.username and not self.email:
            raise ValueError("Either 'username' or 'email' must be provided.")
        return self
    
    model_config = {"extra": "forbid"}

class UserUpdate(SQLModel):
    username: Optional[str] = Field(None, max_length=50)
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    is_verified: Optional[bool] = None
    email: Optional[str] = Field(None, max_length=100)
    
    model_config = {"extra": "forbid"}

# Import here to avoid circular dependency
from src.models.books.models import Book

class UserResponse(BaseUser):
    id: UUID
    is_verified: bool
    books: List = []
    created_at: datetime
    updated_at: Optional[datetime]