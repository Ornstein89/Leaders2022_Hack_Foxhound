from fastapi import APIRouter

from . import file

router = APIRouter(prefix="/api")
router.include_router(file.router)
