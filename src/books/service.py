from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from src.books.models import Book, BookCreate, BookUpdate
from uuid import uuid4,UUID
from datetime import datetime

class BookService:
    async def get_all_books(self, session:AsyncSession):
        result = await session.exec(select(Book).order_by(desc(Book.created_at)))
        books = result.all()
        return books
    async def get_book_by_id(self, book_id: str, session:AsyncSession):
        # statement = select(Book).where(Book.id == book_id)
        # result = await session.exec(select(Book).where(Book.id == book_id))
        # return result.first()
        book = await session.get(Book, book_id)
        return book
    async def create_book(self, book: BookCreate, session:AsyncSession): 
        timestamp_now = datetime.now()   
        new_book_data = book.model_dump()   
        new_book_data.update({
            "id": uuid4(),   
            "created_at": timestamp_now,
            "updated_at": timestamp_now   
        })
        new_book = Book(**new_book_data)
        session.add(new_book)
        await session.commit()
        await session.refresh(new_book)
        return new_book
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
        await session.refresh(book)
        return book
    async def delete_book(self, book_id: str, session:AsyncSession):
        book = await session.get(Book, book_id)
        if not book:
            return None
        await session.delete(book)
        await session.commit()
        return book