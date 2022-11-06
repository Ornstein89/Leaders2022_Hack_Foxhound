from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.database.file import GenerationStatus, GeneratorType


class FileList(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    preview: Optional[str]
    name: str
    dttm_created: datetime
    dttm_updated: datetime
    is_marked_up: bool
    origin_path: Optional[str]
    generation_status: Optional[GenerationStatus]


class GenerateFileParams(BaseModel):
    origin_path: str
    generator_type: GeneratorType
    params: dict


class GenerationFileStatus(BaseModel):
    status: GenerationStatus
