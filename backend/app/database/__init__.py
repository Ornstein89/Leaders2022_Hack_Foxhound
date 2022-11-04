import motor.motor_asyncio
from beanie import init_beanie, sync
from pymongo import MongoClient

from app.config import settings
from app.database.file import File, FileSync


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.database_uri)

    await init_beanie(database=client.db, document_models=[File])


def init_sync_db():
    client = MongoClient(settings.database_uri)
    sync.init_beanie(client.db, document_models=[FileSync])
