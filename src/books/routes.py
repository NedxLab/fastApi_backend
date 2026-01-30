from fastapi import APIRouter, Header, HTTPException, status, Depends
from src.books.models import Book, BookCreate, BookResponse,BookUpdate
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService 
from uuid import UUID
from src.auth.dependencies import AccessTokenBearer, RoleChecker

book_router = APIRouter()
book_service = BookService()
token_auth = AccessTokenBearer()
role_checker = Depends(RoleChecker(allowed_roles=["admin" ]))
@book_router.get("/", dependencies=[role_checker])
async def get_books(session:AsyncSession=Depends(get_session), user_auth=Depends(token_auth)): 
    books = await book_service.get_all_books(session)
    return {"books": books}

@book_router.get("/{book_id}", dependencies=[role_checker])
async def get_book(book_id: str, session:AsyncSession=Depends(get_session), user_auth=Depends(token_auth)):
    book = await book_service.get_book_by_id(book_id, session)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {"book": book}

@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookResponse)
async def create_book(book: BookCreate, session:AsyncSession=Depends(get_session), user_auth=Depends(token_auth)):
    new_book = await book_service.create_book(book, session)
    return {"book": new_book}

@book_router.patch("/{book_id}",status_code=status.HTTP_200_OK, response_model=BookResponse)
async def update_book(book_id: UUID, book_data: BookUpdate, session:AsyncSession=Depends(get_session), user_auth=Depends(token_auth)):
    updated_book = await book_service.update_book(book_id, book_data, session)
    if not updated_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {"book": updated_book}

@book_router.delete("/{book_id}")
async def delete_book(book_id: str, session:AsyncSession=Depends(get_session), user_auth=Depends(token_auth)): 
    deleted_book = await book_service.delete_book(book_id, session)
    if not deleted_book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return {"message": "Book deleted successfully"}