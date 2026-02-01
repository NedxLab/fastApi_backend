from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
import time
import logging 
from fastapi.responses import JSONResponse

logger = logging.getLogger("uvicorn.access") 
logger.disabled = True

def register_middleware(app: FastAPI):
    @app.middleware("http")
    async def custom_logging_middleware(request:Request, call_next):
        start_time = time.time()
        processing_time = time.time() - start_time
        response = await call_next(request)
        message = f"Request: {request.method} - {request.url.path} - {request.client} -{response.status_code} - completed in {processing_time}s "
        print(message)
        return response
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ) 