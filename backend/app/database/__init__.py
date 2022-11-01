import motor.motor_asyncio
from beanie import init_beanie

from app.config import settings
from app.database.file import File


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.database_uri)

    await init_beanie(database=client.db_name, document_models=[File])
