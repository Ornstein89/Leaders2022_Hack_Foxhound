import dramatiq
from beanie import PydanticObjectId
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from app.config import settings
from app.database import FileSync, init_sync_db
from app.database.file import GenerationStatus

dramatiq.set_broker(RabbitmqBroker(url=settings.broker_uri))
init_sync_db()


@dramatiq.actor
def generate_file(_id: str):
    file = FileSync.get(document_id=PydanticObjectId(_id)).run()
    file.generation_status = GenerationStatus.processing
    file.save()
    print(file)

    file.generation_status = GenerationStatus.ready
    file.save()
