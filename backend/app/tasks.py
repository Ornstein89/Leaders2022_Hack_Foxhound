import traceback

import dramatiq
from beanie import PydanticObjectId
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from PIL.Image import fromarray

from app.config import settings
from app.database import FileSync, init_sync_db
from app.database.file import GenerationStatus, GeneratorType
from app.services import FileService

dramatiq.set_broker(RabbitmqBroker(url=settings.broker_uri))
init_sync_db()


@dramatiq.actor
def generate_file(_id: str):
    file = FileSync.get(document_id=PydanticObjectId(_id)).run()
    file.generation_status = GenerationStatus.processing
    file.save()
    file_service = FileService()
    try:
        if file.generator_type == GeneratorType.pix2pix:
            from pix2pix.pix2pix import Pix2Pix

            generator = Pix2Pix(
                "/data/generator.h5", "/data/generator.json", "/data/masks/"
            )
            result, _ = generator.inference(file.origin_path)
            result_path = file_service.save_file_sync(fromarray(result), ext=".png")
            file.paths = [result_path]
        elif file.generator_type == GeneratorType.simple:
            pass
    except Exception:
        file.generation_status = GenerationStatus.error
        file.save()
        print(traceback.format_exc())
        return

    file.generation_status = GenerationStatus.ready
    file.save()
