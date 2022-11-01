import aiofiles
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, UploadFile

from app import database
from app.schemes.file import FileList
from app.utils import generate_file_path, get_or_404

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.get("/", response_model=list[FileList])
async def get_files(limit: int = 10, offset: int = 0):
    return await database.File.aggregate(
        aggregation_pipeline=[
            {"$sort": {"dttm_updated": -1}},
            {"$skip": offset},
            {"$limit": limit},
            {
                "$addFields": {
                    "is_marked_up": {
                        "$switch": {
                            "branches": [
                                {"case": {"$eq": ["$markup", None]}, "then": False}
                            ],
                            "default": True,
                        }
                    }
                }
            },
        ],
        projection_model=FileList,
    ).to_list()


@router.get("/{id}/", response_model=database.File)
async def get_file(id: PydanticObjectId):
    return await get_or_404(database.File, id, "Файл не найден")


@router.post("/", response_model=database.File)
async def create_file(file: UploadFile, name: str = Body()):
    path = generate_file_path()
    async with aiofiles.open(path, "wb") as f:
        content = await file.read()
        await f.write(content)
    return await database.File(path=path, name=name).save()
