import json
from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status
from fastapi.responses import Response

from app import database
from app.schemes.file import FileList
from app.services import FileService
from app.utils import get_or_404

router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.get("/", response_model=list[FileList], response_model_by_alias=False)
async def get_files(
    limit: int = 10,
    offset: int = 0,
    order: str = "-dttm_updated",
    search: Optional[str] = None,
    file_service: FileService = Depends(),
):

    return await file_service.get_list(limit, offset, order, search)


@router.get("/{id}/", response_model=database.File)
async def get_file(id: PydanticObjectId):
    return await get_or_404(database.File, id, "Файл не найден")


@router.get("/{id}/markup/", response_model=database.File)
async def get_file_markup(id: PydanticObjectId):
    file = await get_or_404(database.File, id, "Файл не найден")
    if file.markup is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У файла отсутствует разметка",
        )
    return Response(
        json.dumps(file.markup, indent=4),
        headers={
            "content-disposition": f'attachment; filename="{file.name}_markup.json"'
        },
        media_type="application/json",
    )


@router.post("/", response_model=database.File)
async def create_file(
    file: UploadFile, name: str = Body(), file_service: FileService = Depends()
):
    return await file_service.create(file, name)
