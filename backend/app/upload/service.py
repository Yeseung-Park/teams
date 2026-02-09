from uuid import uuid4
from fastapi import HTTPException, UploadFile, status
import boto3
from app.core.config import settings

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB


class UploadService:
    async def upload_image(self, store_id: int, file: UploadFile) -> str:
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Allowed: JPEG, PNG, WebP")
        
        content = await file.read()
        if len(content) > MAX_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large. Max 5MB")
        
        await file.seek(0)
        
        ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        key = f"menus/{store_id}/{uuid4()}.{ext}"
        
        s3 = boto3.client("s3", region_name=settings.aws_region)
        s3.put_object(
            Bucket=settings.aws_s3_bucket,
            Key=key,
            Body=content,
            ContentType=file.content_type
        )
        
        return f"https://{settings.aws_s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{key}"
