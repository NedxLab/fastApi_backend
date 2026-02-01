from fastapi import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from typing import Optional, Any,Callable
from fastapi import FastAPI, status
from sqlalchemy.exc import SQLAlchemyError
class CustomErrorException(Exception):
    pass
class UserNotFoundException(CustomErrorException):
    """
    Exception raised when a user is not found.
    """
    pass
        
class InvalidTokenException(CustomErrorException):
    def __init__(self):
        """
        Initializes the InvalidTokenException with a default message and status code of 401.
        """
         

class InvalidCredentialsException(CustomErrorException):
    def __init__(self):
        """
        Initializes the InvalidCredentialsException with a default message and status code of 401.
        """
        super().__init__("Invalid credentials", status_code=401)
class UserAlreadyExistsException(CustomErrorException):
    def __init__(self):
        """
        Initializes the UserAlreadyExistsException with a default message and status code of 409.
        """
         
        
class RefreshTokenNotFoundException(CustomErrorException):
    def __init__(self):
        """
        Initializes the RefreshTokenNotFoundException with a default message and status code of 404.
        """
         
class RevokedTokenException(CustomErrorException):
    def __init__(self):
        """
        Initializes the RevokedTokenException with a default message and status code of 403.
        """
         
class AccessTokenRequiredException(CustomErrorException):
    def __init__(self):
        """
        Initializes the AccessTokenRequiredException with a default message and status code of 403.
        """
        
        
class InsufficientPermissionsException(CustomErrorException):
    def __init__(self):
        """
        Initializes the InsufficientPermissionsException with a default message and status code of 403.
        """
         
        
        
def create_exception_handler(status_code:int, detail:Any)->Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc: CustomErrorException):
        return JSONResponse(content={"status_code": status_code, "message": detail}, status_code=status_code)
    return exception_handler
     


def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        UserAlreadyExistsException,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "User with email already exists",
                "error_code": "user_exists",
            },
        ),
    )

    app.add_exception_handler(
        UserNotFoundException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "User not found",
                "error_code": "user_not_found",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenNotFoundException,
        create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Book not found",
                "error_code": "book_not_found",
            },
        ),
    )
    app.add_exception_handler(
        InvalidCredentialsException,
        create_exception_handler(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Invalid Email Or Password",
                "error_code": "invalid_email_or_password",
            },
        ),
    )
    app.add_exception_handler(
        InvalidTokenException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token is invalid Or expired",
                "resolution": "Please get new token",
                "error_code": "invalid_token",
            },
        ),
    )
    app.add_exception_handler(
        RevokedTokenException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Token is invalid or has been revoked",
                "resolution": "Please get new token",
                "error_code": "token_revoked",
            },
        ),
    )
    app.add_exception_handler(
        AccessTokenRequiredException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "Please provide a valid access token",
                "resolution": "Please get an access token",
                "error_code": "access_token_required",
            },
        ),
    )
    app.add_exception_handler(
        RefreshTokenNotFoundException,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Please provide a valid refresh token",
                "resolution": "Please get an refresh token",
                "error_code": "refresh_token_required",
            },
        ),
    )
    app.add_exception_handler(
        InsufficientPermissionsException,
        create_exception_handler(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "message": "You do not have enough permissions to perform this action",
                "error_code": "insufficient_permissions",
            },
        ),
    )
    
 

    @app.exception_handler(500)
    async def internal_server_error(request, exc):

        return JSONResponse(
            content={
                "message": "Internal Server Error",
                "error_code": 500,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


    @app.exception_handler(SQLAlchemyError)
    async def database__error(request, exc):
        print(str(exc))
        return JSONResponse(
            content={
                "message": "Oops! Something went wrong",
                "error_code": 500,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )