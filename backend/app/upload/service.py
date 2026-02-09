from uuid import uuid4
from pathlib import Path
from fastapi import HTTPException, UploadFile, status
import aiofiles

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_SIZE = 5 * 1024 * 1024  # 5MB
UPLOAD_DIR = Path("/app/uploads")


class UploadService:
    async def upload_image(self, store_id: int, file: UploadFile) -> str:
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type. Allowed: JPEG, PNG, WebP")
        
        content = await file.read()
        if len(content) > MAX_SIZE:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File too large. Max 5MB")
        
        # Create store directory
        store_dir = UPLOAD_DIR / str(store_id)
        store_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        filename = f"{uuid4()}.{ext}"
        file_path = store_dir / filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Return URL path
        return f"/uploads/{store_id}/{filename}"
