from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine 
from src.config import Config
from src.models.books.models import Book
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

engine = create_engine(url=Config.DATABASE_URL,  future=True)    
async_engine = AsyncEngine(engine)

async def init_db():
    async with async_engine.begin() as conn:
        from src.models.books.models import Book
        from src.models.auth.models import User
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() ->AsyncSession:
    Session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)
    
    async with Session() as session:
        yield session