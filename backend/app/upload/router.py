from fastapi import APIRouter, Depends, UploadFile, File
from app.core.dependencies import get_current_admin
from app.auth.schemas import TokenPayload
from app.upload.service import UploadService

router = APIRouter(prefix="/admin/upload", tags=["upload"])
upload_service = UploadService()


@router.post("/image")
async def upload_image(file: UploadFile = File(...), user: TokenPayload = Depends(get_current_admin)):
    url = await upload_service.upload_image(user.store_id, file)
    return {"image_url": url}
