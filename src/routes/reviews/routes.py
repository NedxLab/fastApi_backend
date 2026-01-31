from typing import List
from fastapi import APIRouter, Header, HTTPException, status, Depends 
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession 
from uuid import UUID
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.services.reviews.services import ReviewService
from src.models.reviews.schemas import ReviewResponse, CreateReviews,ReviewBasicResponse



reviews_router = APIRouter()
review_service = ReviewService()
token_auth = AccessTokenBearer()

@reviews_router.get("/", status_code=status.HTTP_200_OK, response_model=list[ReviewResponse])
async def get_reviews(session:AsyncSession=Depends(get_session), user_details=Depends(token_auth)): 
    reviews = await review_service.get_all_reviews(session)
    return reviews
@reviews_router.get("/{book_id}", status_code=status.HTTP_200_OK )
async def get_review_by_id(book_id: str, session:AsyncSession=Depends(get_session), user_details=Depends(token_auth)):  
    review = await review_service.get_reviews_by_book_id(book_id, session) 
    return review
@reviews_router.post("/", status_code=status.HTTP_201_CREATED, response_model=list[ReviewBasicResponse])
async def create_review(review: CreateReviews, session:AsyncSession=Depends(get_session), user_details=Depends(token_auth)): 
    review = await review_service.create_review(review, session, user_details)
    return [review]