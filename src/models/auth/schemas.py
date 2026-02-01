from datetime import datetime
from uuid import UUID
from typing import List, Optional
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, String
from pydantic import model_validator ,BaseModel

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
   
    email: str = Field(
        sa_column=Column(String(100), unique=True, nullable=False)
    )

class CreateUser(BaseUser):
    password: str = Field(
        sa_column=Column(String(255), nullable=False),  exclude=True
    )

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
 

class UserResponse(BaseUser):
    id: UUID
    is_verified: bool
    books: List = []
    reviews: List = []
    created_at: datetime
    updated_at: Optional[datetime]

class UserBasicResponse(BaseUser):
    id: UUID
    is_verified: bool 
    created_at: datetime
    updated_at: Optional[datetime]

class EmailModel(BaseModel):
    addresses: List[str] 