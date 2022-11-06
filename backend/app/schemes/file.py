from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.database.file import GenerationStatus, Location, PathologyType


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
    research_type: Optional[str]
    pathology: Optional[PathologyType]
    generator_type: Optional[str]
    size: Optional[int]
    location: Optional[Location]


class GenerationFileStatus(BaseModel):
    status: GenerationStatus
