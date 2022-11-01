from datetime import datetime
from enum import Enum
from typing import Optional

from beanie import Document
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


class Location(BaseModel):
    vertical: VerticalLocation
    horizontal: HorizontalLocation


class File(Document):
    path: str
    name: str
    dttm_created: datetime = Field(default_factory=datetime.now)
    dttm_updated: datetime = Field(default_factory=datetime.now)
    preview: Optional[str]
    origin_path: Optional[str]
    markup: Optional[dict]
    research_type: Optional[str]
    pathology: Optional[PathologyType]
    generator_type: Optional[str]
    size: Optional[int]
    location: Optional[Location]

    class Settings:
        name = "file_collection"
