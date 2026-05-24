from fastapi import APIRouter, UploadFile, File

from src.service.file_service import FileService

file_service = FileService()
file_router = APIRouter()

@file_router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    upload_result = await file_service.upload_to_s3(file)
    return upload_result