from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc
from sqlalchemy.orm import selectinload
from src.models.reviews.models import Reviews
from src.models.reviews.schemas import CreateReviews
from uuid import uuid4,UUID
from datetime import datetime
from src.models.books.models import Book


class ReviewService:
    async def get_all_reviews(self, session:AsyncSession) -> list[Reviews]:
        stmt = select(Reviews).options(selectinload(Reviews.user),selectinload(Reviews.book)).order_by(desc(Reviews.created_at))
        result = await session.exec(stmt)
        reviews = result.all()
        return reviews
    async def get_reviews_by_book_id(
    self,
    book_id: UUID,
    session: AsyncSession) -> list[Reviews]:

        stmt = (
            select(Reviews)
            .where(Reviews.book_id == book_id)
            .options(
                selectinload(Reviews.user),
                selectinload(Reviews.book),
            )
            .order_by(desc(Reviews.created_at))
        )

        result = await session.exec(stmt)
        return result.all()
    async def create_review(self, reviews: CreateReviews   , session:AsyncSession, token_details: dict): 
        timestamp_now = datetime.now()   
        new_reviews_data = reviews.model_dump()   
        new_reviews_data.update({
            "id": uuid4(),   
            "created_by": token_details["sub"],
            "created_at": timestamp_now,
            "updated_at": timestamp_now
        }) 
        new_reviews = Reviews(**new_reviews_data)
        session.add(new_reviews)
        await session.commit()
        await session.refresh(new_reviews, attribute_names=["user"])
        return new_reviews