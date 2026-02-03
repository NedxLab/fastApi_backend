from celery import Celery
from src.config import broker_url, result_backend
from src.mail import mail, create_message
from pydantic import EmailStr
from asgiref.sync import async_to_sync

# Create Celery app with broker and backend
c_app = Celery("fastapi_tasks", broker=broker_url, backend=result_backend)
c_app.config_from_object("src.config")


@c_app.task(name="send_background_email")
def send_background_email(email: list[str], subject: str, body: str): 
    message = create_message(receipient=email, subject=subject, body=body) 
    res = async_to_sync(mail.send_message)(message) 
    return res