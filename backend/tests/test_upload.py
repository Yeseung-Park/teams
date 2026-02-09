import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.upload.service import UploadService
from fastapi import HTTPException, UploadFile
from io import BytesIO


@pytest.fixture
def upload_service():
    return UploadService()


# TC-UPLOAD-001: 유효한 이미지 업로드
@pytest.mark.asyncio
async def test_upload_image_valid(upload_service):
    mock_file = MagicMock(spec=UploadFile)
    mock_file.content_type = "image/jpeg"
    mock_file.filename = "test.jpg"
    mock_file.read = AsyncMock(return_value=b"fake image data")
    mock_file.seek = AsyncMock()
    
    with patch('app.upload.service.boto3') as mock_boto:
        mock_s3 = MagicMock()
        mock_boto.client.return_value = mock_s3
        
        result = await upload_service.upload_image(1, mock_file)
    
    assert result.startswith("https://")
    assert ".s3." in result


# TC-UPLOAD-002: 잘못된 파일 형식 업로드 실패
@pytest.mark.asyncio
async def test_upload_image_invalid_type(upload_service):
    mock_file = MagicMock(spec=UploadFile)
    mock_file.content_type = "application/pdf"
    mock_file.filename = "test.pdf"
    
    with pytest.raises(HTTPException) as exc_info:
        await upload_service.upload_image(1, mock_file)
    
    assert exc_info.value.status_code == 400
