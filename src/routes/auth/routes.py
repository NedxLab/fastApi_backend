from fastapi import APIRouter, Header, HTTPException, status, Depends 
from src.auth.dependencies import AccessTokenBearer, RefreshTokenBearer, RoleChecker,get_current_user
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession 
from uuid import UUID
from src.models.auth.models import User
from src.models.auth.schemas import CreateUser, LoginUser, UserResponse,EmailModel
from src.services.auth.services import AuthService
from src.mail import mail, create_message
from src.config import Config
from src.auth.utils import create_url_safe_token
from pydantic import EmailStr

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
    token = create_url_safe_token({"email": new_user.email})
    link = f"http://{Config.SERVER_URL}/api/v1/auth/verify/{token}"

    html_message = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8" />
    <title>Verify Email</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, Helvetica, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
        <td align="center" style="padding:40px 0;">
            <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; padding:30px;">
            
            <tr>
                <td style="text-align:center;">
                <h1 style="color:#333333; margin-bottom:10px;">
                    Verify your email
                </h1>
                <p style="color:#555555; font-size:16px; line-height:1.5;">
                    Thanks for signing up! Please confirm your email address by clicking the button below.
                </p>
                </td>
            </tr>

            <tr>
                <td align="center" style="padding:30px 0;">
                <a href="{link}"
                    style="
                    background-color:#2563eb;
                    color:#ffffff;
                    text-decoration:none;
                    padding:14px 24px;
                    border-radius:6px;
                    font-size:16px;
                    display:inline-block;
                    ">
                    Verify Email
                </a>
                </td>
            </tr>

            <tr>
                <td style="color:#777777; font-size:14px; line-height:1.5;">
                <p>
                    If the button doesn’t work, copy and paste this link into your browser:
                </p>
                <p style="word-break:break-all; color:#2563eb;">
                    {link}
                </p>
                </td>
            </tr>

            <tr>
                <td style="padding-top:30px; color:#999999; font-size:12px; text-align:center;">
                <p>
                    If you didn’t create an account, you can safely ignore this email.
                </p>
                </td>
            </tr>

            </table>
        </td>
        </tr>
    </table>
    </body>
    </html>
    """
    await user_service.send_email(new_user.email,  html_message )
    return new_user

@auth_router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_user(login_data: LoginUser, session:AsyncSession=Depends(get_session)): 
    jsonResponse = await user_service.authenticate_user(login_data, session)
    if not jsonResponse:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return jsonResponse
@auth_router.post("/verify/{token}", status_code=status.HTTP_200_OK)
async def verify_user(token:str, session:AsyncSession=Depends(get_session)): 
    await user_service.verify_user(token, session)
    return {"message": "Email Verified successfully"}
@auth_router.post("/change-password/{token}", status_code=status.HTTP_200_OK)
async def change_password(token:str,newPassword:str, session:AsyncSession=Depends(get_session)): 
    await user_service.change_password(token,newPassword, session)
    return {"message": "Password Changed successfully"}
@auth_router.post("/reset-password/{email}", status_code=status.HTTP_200_OK)
async def reset_password(email:EmailStr, session:AsyncSession=Depends(get_session)): 
    token = create_url_safe_token({"email": email})
    link = f"http://{Config.SERVER_URL}/api/v1/auth/change-password/{token}"

    html_message = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <title>Password Reset</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f4f6f8; font-family:Arial, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0">
        <tr>
            <td align="center" style="padding:40px 0;">
            <table width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:8px; overflow:hidden;">
                <tr>
                <td style="padding:30px; text-align:center;">
                    <h2 style="color:#333;">Reset Your Password</h2>

                    <p style="color:#555; font-size:15px; line-height:1.6;">
                    We received a request to reset your password. Click the button below to continue.
                    </p>

                    <a href="{link}"
                    style="
                        display:inline-block;
                        margin:25px 0;
                        padding:14px 28px;
                        background-color:#2563eb;
                        color:#ffffff;
                        text-decoration:none;
                        border-radius:6px;
                        font-weight:bold;
                    ">
                    Reset Password
                    </a>

                    <p style="color:#777; font-size:14px;">
                    This link will expire soon for security reasons.
                    </p>

                    <p style="color:#999; font-size:13px; margin-top:30px;">
                    If you did not request a password reset, please ignore this email.
                    </p>

                    <hr style="margin:30px 0; border:none; border-top:1px solid #eee;" />

                    <p style="color:#aaa; font-size:12px;">
                    © {Config.SERVER_URL} — All rights reserved
                    </p>
                </td>
                </tr>
            </table>
            </td>
        </tr>
        </table>
    </body>
    </html>
    """
    await user_service.send_email(email,  html_message )
    return {"message": "Password Reset link sent successfully"}

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