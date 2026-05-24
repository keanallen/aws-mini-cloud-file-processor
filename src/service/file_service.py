import datetime

from fastapi import UploadFile
from src import utils


class FileService:
    
    async def upload_to_s3(self, file: UploadFile):
        if file is None or not file.filename:
            return {"success": False, "message": "No file uploaded"}
        if file.size and file.size > 10 * 1024 * 1024:
            return {"success": False, "message": "File size exceeds 10MB limit"}
        # upload file to S3
        uuid = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        ext = file.filename.split(".")[-1]
        object_name = f"{uuid}.{ext}"
        success = await utils.upload_file_to_s3(file, object_name)
        if success:
            return {"success": True, "message": "File uploaded successfully"}
        else:
            return {"success": False, "message": "Error uploading file"}