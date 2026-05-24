
from fastapi import APIRouter
from src.api.v1.file import file_router


api_router = APIRouter()

api_router.include_router(file_router, prefix="/file", tags=["file"])
