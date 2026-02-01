from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from src.config import Config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

conf = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM_EMAIL,
    MAIL_PORT=Config.MAIL_PORT,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,    
    MAIL_SSL_TLS=False,   
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER= Path(BASE_DIR, "templates/email"),
    )

mail = FastMail(conf)

def create_message(receipient:list[str], body:str, subject:str):
    message = MessageSchema(
        subject=subject,
        recipients=receipient,
        body=body,
        subtype=MessageType.html
    )
    return message
 