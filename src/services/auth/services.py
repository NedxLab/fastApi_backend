from ...models.auth.models import User, CreateUser, LoginUser, UserUpdate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select,desc 
from sqlalchemy.orm import selectinload
from uuid import uuid4,UUID
from datetime import datetime,timedelta
from ...auth.utils import hash_password, verify_password
from ...auth.utils import create_access_token, decode_access_token
from fastapi.responses import JSONResponse


class AuthService:
    async def user_exists(self, username: str, email: str, session: AsyncSession) -> bool:
        query = select(User).where((User.username == username) | (User.email == email))
        result = await session.exec(query)
        existing_user = result.first()
        return existing_user is not None
    async def register_user(self, user_data: CreateUser, session: AsyncSession) -> User:
        hashed_password = hash_password(user_data.password)
        isUserExist = await self.user_exists(user_data.username, user_data.email, session)
        if isUserExist:
            return None
        new_user = User(
            id=uuid4(),
            **user_data.model_dump(exclude={"password"}),
            hashed_password=hashed_password,
            role="user",
            created_at=datetime.now()
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    async def authenticate_user(self, login_data: LoginUser, session: AsyncSession) -> User | None:
        query = select(User)
        if login_data.username:
            query = query.where(User.username == login_data.username)
        elif login_data.email:
            query = query.where(User.email == login_data.email)
        result = await session.exec(query)
        user = result.first()
        if user:
            password_valid = verify_password(login_data.password, user.hashed_password)
            if password_valid:
                access_token = create_access_token(data={"sub": str(user.id), "username": user.username, "email": user.email, "role": user.role})
                refresh_token = create_access_token(data={"sub": str(user.id), "username": user.username, "email": user.email, "role": user.role},refresh =True, expires_delta= timedelta(days=7))
                return JSONResponse(content={"access_token": access_token, "refresh_token": refresh_token, "message": "Authentication successful", "user": str(user.model_dump(exclude={"hashed_password","created_at","updated_at"}))})
        return None

    async def update_user(self, user_id: UUID, user_data: UserUpdate, session: AsyncSession) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await session.exec(query)
        user = result.first()
        if not user:
            return None
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        user.updated_at = datetime.now()
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def get_user_by_id(self, user_id: UUID, session: AsyncSession) -> User | None:
       stmt = (
        select(User)
        .options(selectinload(User.books))
        .where(User.id == user_id)
       )
       result = await session.exec(stmt)
       return result.first()
    
    async def get_user_by_username(self, username: str, session: AsyncSession) -> User | None:
        query = select(User).where(User.username == username)
        result = await session.exec(query)
        return result.first()
    
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User | None:
        query = select(User).where(User.email == email)
        result = await session.exec(query)
        return result.first()
    
    async def get_new_access_token(self, user_details: dict, session: AsyncSession) -> str | None: 
        user_id = user_details.get("sub")
        query = select(User).where(User.id == UUID(user_id))
        result = await session.exec(query)
        user = result.first()
        if not user:
            return None
        
        new_access_token = create_access_token(data={"sub": str(user.id), "username": user.username, "email": user.email, "role": user.role})
        return new_access_token
    async def logout_user(self, user_details: dict, session: AsyncSession) -> bool:
        jti = user_details.get("jti")
        if not jti:
            return False
        from src.db.redis import add_jti_to_blocklist
        await add_jti_to_blocklist(jti)
        return True