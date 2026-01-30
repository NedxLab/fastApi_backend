from fastapi import FastAPI
from src.routes.books.routes import book_router
from src.routes.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Starting up the {app.title} application...")
    await init_db()
    yield
    print(f"Shutting down the {app.title} application...")
version = "v1"
app = FastAPI(
    title="Book API",
    description="An API to manage books",
    version=version, 
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])