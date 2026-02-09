import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from app.auth.service import AuthService
from fastapi import HTTPException


@pytest.fixture
def auth_service():
    return AuthService()


@pytest.fixture
def mock_db():
    return AsyncMock()


# TC-AUTH-001: 유효한 자격증명으로 테이블 로그인
@pytest.mark.asyncio
async def test_login_table_with_valid_credentials(auth_service, mock_db):
    from app.models.models import Store, Table
    
    mock_store = MagicMock(spec=Store)
    mock_store.store_id = 1
    
    mock_table = MagicMock(spec=Table)
    mock_table.table_id = 1
    mock_table.store_id = 1
    mock_table.table_password_hash = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.G5e5e5e5e5e5e5"
    
    mock_result_store = MagicMock()
    mock_result_store.scalar_one_or_none.return_value = mock_store
    
    mock_result_table = MagicMock()
    mock_result_table.scalar_one_or_none.return_value = mock_table
    
    mock_db.execute = AsyncMock(side_effect=[mock_result_store, mock_result_table])
    
    with patch('app.auth.service.pwd_context') as mock_pwd:
        mock_pwd.verify.return_value = True
        result = await auth_service.login_table(mock_db, "test-store", 1, "password123")
    
    assert result.access_token is not None
    assert result.token_type == "bearer"


# TC-AUTH-002: 잘못된 비밀번호로 테이블 로그인 실패
@pytest.mark.asyncio
async def test_login_table_with_invalid_password(auth_service, mock_db):
    from app.models.models import Store, Table
    
    mock_store = MagicMock(spec=Store)
    mock_store.store_id = 1
    
    mock_table = MagicMock(spec=Table)
    mock_table.table_id = 1
    mock_table.table_password_hash = "$2b$12$hash"
    
    mock_result_store = MagicMock()
    mock_result_store.scalar_one_or_none.return_value = mock_store
    
    mock_result_table = MagicMock()
    mock_result_table.scalar_one_or_none.return_value = mock_table
    
    mock_db.execute = AsyncMock(side_effect=[mock_result_store, mock_result_table])
    
    with patch('app.auth.service.pwd_context') as mock_pwd:
        mock_pwd.verify.return_value = False
        with pytest.raises(HTTPException) as exc_info:
            await auth_service.login_table(mock_db, "test-store", 1, "wrongpassword")
    
    assert exc_info.value.status_code == 401


# TC-AUTH-003: 유효한 자격증명으로 관리자 로그인
@pytest.mark.asyncio
async def test_login_admin_with_valid_credentials(auth_service, mock_db):
    from app.models.models import Store
    
    mock_store = MagicMock(spec=Store)
    mock_store.store_id = 1
    mock_store.admin_password_hash = "$2b$12$hash"
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_store
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    with patch('app.auth.service.pwd_context') as mock_pwd:
        mock_pwd.verify.return_value = True
        result = await auth_service.login_admin(mock_db, "test-store", "admin", "adminpass")
    
    assert result.access_token is not None


# TC-AUTH-004: 유효한 토큰 검증
def test_verify_token_with_valid_token(auth_service):
    with patch('app.auth.service.jwt') as mock_jwt:
        mock_jwt.decode.return_value = {"store_id": 1, "table_id": 1, "is_admin": False}
        result = auth_service.verify_token("valid_token")
    
    assert result.store_id == 1
    assert result.table_id == 1
    assert result.is_admin == False


# TC-AUTH-005: 잘못된 토큰 검증 실패
def test_verify_token_with_invalid_token(auth_service):
    from jose import JWTError
    
    with patch('app.auth.service.jwt') as mock_jwt:
        mock_jwt.decode.side_effect = JWTError()
        with pytest.raises(HTTPException) as exc_info:
            auth_service.verify_token("invalid_token")
    
    assert exc_info.value.status_code == 401
