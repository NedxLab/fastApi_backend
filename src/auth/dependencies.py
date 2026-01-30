from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException, status, Request
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_access_token
from src.db.redis import check_jti_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession 
from .services import AuthService
from uuid import uuid4,UUID

user_service = AuthService()
class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)
        if credentials:
            token= credentials.credentials 
            user_details = self.token_valid(token)
            if not user_details:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
            if await check_jti_in_blocklist(user_details.get("jti")):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token has been revoked.")           
            return user_details
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authentication credentials")
        
    def token_valid(self, token: str) -> bool:
        decoded_token = decode_access_token(token) 
        return True if decoded_token else False

class AccessTokenBearer(TokenBearer):
    def token_valid(self, token: str) -> dict:
        decoded_token = decode_access_token(token)
        if decoded_token :
            if decoded_token and not decoded_token.get("refresh", False):
                return decoded_token
            elif decoded_token.get("refresh", False):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Provided token is a refresh token, access token required.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired token.")
  

class RefreshTokenBearer(TokenBearer):
    def token_valid(self, token: str) -> dict:
        decoded_token = decode_access_token(token)
        if decoded_token and decoded_token.get("refresh", False):
            return decoded_token
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Provided token is not a refresh token.")


async def get_current_user(token: str = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    user_details =  token
    user = await user_service.get_user_by_id(UUID(user_details.get("sub")), session)
    return user

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    async def __call__(self, user: dict = Depends(AccessTokenBearer())):
        user_role = user.get("role")
        if user_role not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to access this resource.")
        return True