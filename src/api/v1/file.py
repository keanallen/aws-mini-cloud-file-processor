
from fastapi import APIRouter, Body
from src.schemas.file_schema import UploadFileRequest

file_router = APIRouter()

@file_router.post("/upload")
async def upload_file(file: UploadFileRequest =Body(..., embed=True)):
    return {"filename": file.file.filename}