from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from sqlalchemy.orm import selectinload
from src.models.books.models import Book
from src.models.books.schemas import BookCreate, BookUpdate
from uuid import uuid4,UUID
from datetime import datetime

class BookService:
    async def get_all_books(self, session:AsyncSession) -> list[Book]:
        stmt = select(Book).options(selectinload(Book.user)).order_by(desc(Book.created_at))
        result = await session.exec(stmt)
        books = result.all()
        return books
    async def get_book_by_id(self, book_id: str, session:AsyncSession): 
        stmt = select(Book).options(selectinload(Book.user)).where(Book.id == book_id)
        result = await session.exec(stmt)
        return result.first()
    async def create_book(self, book: BookCreate, session:AsyncSession, token_details: dict): 
        timestamp_now = datetime.now()   
        new_book_data = book.model_dump()   
        new_book_data.update({
            "id": uuid4(),   
            "created_by": token_details["sub"],
            "created_at": timestamp_now,
            "updated_at": timestamp_now
        })
        new_book = Book(**new_book_data)
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book, attribute_names=["user"])
        return new_book
    
    async def get_books_by_user(self,  user_id: str, session:AsyncSession):
        print("Fetching books for user_id:", user_id)
        stmt = select(Book).options(selectinload(Book.user),selectinload(Book.reviews)).where(Book.created_by == user_id)
        result = await session.exec(stmt)
        return result.all()
    async def update_book(self, book_id: UUID, book_data: BookUpdate, session:AsyncSession):
        book = await session.get(Book, book_id)  
        if not book:
            return None
        for key, value in book_data.model_dump().items():
            if value is not None:
                setattr(book, key, value)
        book.updated_at = datetime.now()
        session.add(book)
        await session.commit()
        await session.refresh(book, attribute_names=["user"])
        return book
    async def delete_book(self, book_id: str, session:AsyncSession):
        book = await session.get(Book, book_id)
        if not book:
            return None
        await session.delete(book)
        await session.commit()
        return book