from fastapi import APIRouter, Header, HTTPException, status, Depends 
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker,get_current_user
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession 
from uuid import UUID
from src.models.auth.models import User
from src.models.auth.schemas import CreateUser, LoginUser, UserResponse
from src.services.auth.services import AuthService


auth_router = APIRouter()

user_service = AuthService()
refresh_token_auth = RefreshTokenBearer()
token_auth = AccessTokenBearer() 
role_checker = RoleChecker(allowed_roles=["admin", "user"])
@auth_router.post("/register", status_code=status.HTTP_201_CREATED, response_model= User)
async def register_user(user_data: CreateUser, session:AsyncSession=Depends(get_session)): 
    new_user = await user_service.register_user(user_data, session)
    if new_user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return {"message": "User registered successfully"}

@auth_router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_user(login_data: LoginUser, session:AsyncSession=Depends(get_session)): 
    jsonResponse = await user_service.authenticate_user(login_data, session)
    if not jsonResponse:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return jsonResponse

@auth_router.get("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_access_token( session:AsyncSession=Depends (get_session), user_details:dict=Depends(refresh_token_auth)):
    new_token = await user_service.get_new_access_token(user_details, session)
    if not new_token:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not refresh access token")
    return {"access_token": new_token}

@auth_router.get('/me', response_model=UserResponse)
async def get_current_user_endpoint(user:User=Depends(get_current_user)):
    return user
@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user( session:AsyncSession=Depends (get_session), user_details:dict=Depends(token_auth)):
    print(user_details)
    logout_success = await user_service.logout_user(user_details, session)
    if not logout_success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Logout failed")
    return {"message": "Logout successful"}