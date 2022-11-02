from typing import Optional, Type, TypeVar, cast

from beanie import Document, PydanticObjectId
from fastapi import HTTPException, status

T = TypeVar("T", bound=Document)


async def get_or_404(
    model: Type[T], _id: PydanticObjectId, error_msg: Optional[str] = None
) -> T:
    obj = await model.get(document_id=_id)
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error_msg or "Не найдено",
        )
    return cast(type(model), obj)
