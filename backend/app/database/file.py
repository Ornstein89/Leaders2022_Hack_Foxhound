from datetime import datetime
from enum import Enum
from typing import Optional

import pymongo
from beanie import Document, Indexed, sync
from pydantic import BaseModel, Field


class PathologyType(str, Enum):
    covid = "COVID-19"
    cancer = "Рак легкого"
    damage = "Метастатическое поражение лёгких"


class VerticalLocation(str, Enum):
    left = "Левое"
    right = "Правое"


class HorizontalLocation(str, Enum):
    top = "Верхняя"
    middle = "Средняя"
    bottom = "Нижняя"


class GenerationStatus(str, Enum):
    error = "error"
    processing = "processing"
    ready = "ready"


class Location(BaseModel):
    vertical: VerticalLocation
    horizontal: HorizontalLocation


class GeneratorType(str, Enum):
    simple = "simple"
    pix2pix = "pix2pix"


class BaseFile(BaseModel):
    paths: list[str]
    name: Indexed(str, pymongo.TEXT)
    dttm_created: datetime = Field(default_factory=datetime.utcnow)
    dttm_updated: datetime = Field(default_factory=datetime.utcnow)
    preview: Optional[str]
    origin_path: Optional[str]
    markup: Optional[dict]
    research_type: Optional[str]
    pathology: Optional[PathologyType]
    generator_type: Optional[GeneratorType]
    size: Optional[int]
    location: Optional[Location]
    generation_status: Optional[GenerationStatus]
    generation_params: Optional[dict]

    class Settings:
        name = "file_collection"


class File(Document, BaseFile):
    ...


class FileSync(sync.Document, BaseFile):
    ...
