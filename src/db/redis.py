from redis import asyncio as aioredis
from src.config import Config

JTI_EXPIRY = 3600

# Create Redis client
token_blocklist = aioredis.Redis(
    host=Config.REDIS_HOST, 
    port=Config.REDIS_PORT, 
    db=Config.REDIS_DB, 
    decode_responses=True
)

async def add_jti_to_blocklist(jti: str):
    await token_blocklist.set(name=jti, value="true", ex=JTI_EXPIRY)

async def check_jti_in_blocklist(jti: str) -> bool:
    print("Checking JTI in blocklist:", jti, token_blocklist)
    result = await token_blocklist.exists(jti)
    return result > 0