from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import Config
import jwt
import uuid
import logging
from fastapi import Depends, HTTPException, status, Request


passwordContext = CryptContext(
    schemes=["argon2"], 
    deprecated="auto"
)

def hash_password(password: str) -> str:
    return passwordContext.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return passwordContext.verify(plain_password, hashed_password)

def create_access_token(data: dict, refresh: bool = False, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
        "exp": expire  
    })
    
    token = jwt.encode(
        to_encode,
        Config.JWT_SECRET_KEY,
        algorithm=Config.JWT_ALGORITHM
    )
    return token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET_KEY,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid access token.")
    except jwt.PyJWTError as e:
        logging.error(f"JWT Error: {e}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token decoding error")