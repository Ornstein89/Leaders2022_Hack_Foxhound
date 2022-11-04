from typing import Optional
from uuid import uuid4

import aiofiles
from beanie.odm.operators.find.evaluation import RegEx
from fastapi import HTTPException, UploadFile, status

from app import database
from app.schemes.file import FileList
from app.services.make_dicom_thumbnail import make_dicom_thumbnail

ORDER_FIELDS = {"dttm_updated", "dttm_created", "name"}


class FileService:
    def generate_file_path(self) -> str:
        return f"./media/files/{uuid4()}"

    async def create(self, file: UploadFile, name: str) -> database.File:
        path = self.generate_file_path()
        async with aiofiles.open(path, "wb") as f:
            content = await file.read()
            await f.write(content)
        preview_path = None
        preview = make_dicom_thumbnail(path, (128, 128))
        if preview is not None:
            preview_path = self.generate_file_path() + ".png"
            preview.save(preview_path)
        return await database.File(path=path, name=name, preview=preview_path).save()

    def get_sort(self, field: str) -> dict[str, int]:
        desc = 1
        if field.startswith("-"):
            desc = -1
            field = field[1:]
        if field not in ORDER_FIELDS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Поле {} не является валидным, выберите из {}".format(
                    field, ", ".join(ORDER_FIELDS)
                ),
            )
        return {field: desc}

    async def get_list(
        self, limit: int, offset: int, order: str, search: Optional[str]
    ) -> list[FileList]:
        aggregation_pipeline = [
            {"$sort": self.get_sort(order)},
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
        ]
        query = database.File
        if search:
            query = query.find(RegEx("name", search, options="i"))

        return await query.aggregate(
            aggregation_pipeline=aggregation_pipeline, projection_model=FileList
        ).to_list()
