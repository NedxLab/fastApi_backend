from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    MAIL_USERNAME : str
    MAIL_PASSWORD : str
    MAIL_SERVER : str
    MAIL_PORT : int
    MAIL_FROM_EMAIL :EmailStr
    MAIL_FROM_NAME : str
    SERVER_URL:str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
Config = Settings()

broker_url: str = (
    f"redis://{Config.REDIS_HOST}:{Config.REDIS_PORT}/{Config.REDIS_DB}"
)
result_backend = broker_url
broker_connection_retry_on_startup = True