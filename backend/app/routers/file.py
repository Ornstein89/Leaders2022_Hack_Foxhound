import json
from datetime import datetime
from typing import Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, HTTPException, UploadFile, status
from fastapi.responses import Response

from app import database
from app.database.file import GenerationStatus
from app.schemes.file import FileList, GenerateFileParams, GenerationFileStatus
from app.services import FileService
from app.tasks import generate_file
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


@router.get("/{id}/", response_model=database.File, response_model_by_alias=False)
async def get_file(id: PydanticObjectId):
    return await get_or_404(database.File, id, "Файл не найден")


@router.get("/{id}/markup/")
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


@router.post("/", response_model=database.File, response_model_by_alias=False)
async def create_file(
    files: list[UploadFile], name: str = Body(), file_service: FileService = Depends()
):
    return await file_service.create(files, name)


@router.put(
    "/{id}/markup/", response_model=database.File, response_model_by_alias=False
)
async def save_markup(id: PydanticObjectId, schema: dict):
    file = await get_or_404(database.File, id, "Файл не найден")
    file.markup = schema
    file.dttm_updated = datetime.utcnow()
    await file.save()
    return file


@router.post(
    "/{id}/generate/", response_model=database.File, response_model_by_alias=False
)
async def generate_file_route(id: PydanticObjectId, params: GenerateFileParams):
    origin_file = await get_or_404(database.File, id, "Файл не найден")
    if params.origin_path not in origin_file.paths:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Невалидный путь к файлу"
        )
    file = await database.File(
        **params.dict(), generation_status=GenerationStatus.processing
    ).save()
    generate_file.send(file.id)
    return file


@router.get("/{id}/status/", response_model=GenerationFileStatus)
async def get_generation_status(id: PydanticObjectId):
    file = await get_or_404(database.File, id, "Файл не найден")
    return GenerationFileStatus(status=file.generation_status)
