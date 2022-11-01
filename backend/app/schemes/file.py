from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class FileList(BaseModel):
    id: PydanticObjectId = Field(..., alias="_id")
    preview: Optional[str]
    name: str
    dttm_created: datetime
    dttm_updated: datetime
    is_marked_up: bool
    origin_path: Optional[str]
