import pytest
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock, patch
from app.table.service import TableService
from fastapi import HTTPException


@pytest.fixture
def table_service():
    return TableService()


@pytest.fixture
def mock_db():
    return AsyncMock()


# TC-TABLE-001: 새 세션 생성
@pytest.mark.asyncio
async def test_ensure_session_creates_new(table_service, mock_db):
    from app.models.models import Table, TableSession
    
    mock_table = MagicMock(spec=Table)
    mock_table.table_id = 1
    mock_table.current_session_id = None
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_table
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    
    def mock_refresh(obj):
        if hasattr(obj, 'session_id'):
            obj.session_id = 100
    
    mock_db.refresh = AsyncMock(side_effect=mock_refresh)
    
    result = await table_service.ensure_session(mock_db, 1)
    
    assert result == 100


# TC-TABLE-002: 기존 세션 반환
@pytest.mark.asyncio
async def test_ensure_session_returns_existing(table_service, mock_db):
    from app.models.models import Table
    
    mock_table = MagicMock(spec=Table)
    mock_table.table_id = 1
    mock_table.current_session_id = 50
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_table
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    result = await table_service.ensure_session(mock_db, 1)
    
    assert result == 50


# TC-TABLE-003: 테이블 이용 완료
@pytest.mark.asyncio
async def test_complete_table(table_service, mock_db):
    from app.models.models import Table, TableSession
    
    mock_table = MagicMock(spec=Table)
    mock_table.table_id = 1
    mock_table.store_id = 1
    mock_table.current_session_id = 10
    
    mock_session = MagicMock(spec=TableSession)
    mock_session.session_id = 10
    mock_session.is_active = True
    
    mock_result_table = MagicMock()
    mock_result_table.scalar_one_or_none.return_value = mock_table
    
    mock_result_session = MagicMock()
    mock_result_session.scalar_one_or_none.return_value = mock_session
    
    mock_db.execute = AsyncMock(side_effect=[mock_result_table, mock_result_session])
    mock_db.commit = AsyncMock()
    
    with patch('app.table.service.sse_service') as mock_sse:
        mock_sse.broadcast = AsyncMock()
        await table_service.complete_table(mock_db, 1, 1)
    
    assert mock_table.current_session_id is None
    assert mock_session.is_active == False


# TC-TABLE-004: 활성 세션 없이 완료 시도
@pytest.mark.asyncio
async def test_complete_table_no_session(table_service, mock_db):
    from app.models.models import Table
    
    mock_table = MagicMock(spec=Table)
    mock_table.table_id = 1
    mock_table.store_id = 1
    mock_table.current_session_id = None
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_table
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    with pytest.raises(HTTPException) as exc_info:
        await table_service.complete_table(mock_db, 1, 1)
    
    assert exc_info.value.status_code == 400


# TC-TABLE-005: 테이블 히스토리 조회
@pytest.mark.asyncio
async def test_get_table_history(table_service, mock_db):
    mock_item = MagicMock()
    mock_item.order_item_id = 1
    mock_item.menu_id = 1
    mock_item.menu_name = "Test"
    mock_item.quantity = 1
    mock_item.unit_price = 10000
    mock_item.subtotal = 10000
    
    mock_order = MagicMock()
    mock_order.order_id = 1
    mock_order.order_number = "20260209-0001"
    mock_order.total_amount = 10000
    mock_order.order_status = "completed"
    mock_order.created_at = datetime.now()
    mock_order.items = [mock_item]
    
    mock_session = MagicMock()
    mock_session.session_id = 1
    mock_session.is_active = False
    mock_session.orders = [mock_order]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_session]
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    result = await table_service.get_table_history(mock_db, 1, 1, None)
    
    assert len(result) == 1
    assert result[0].order_id == 1
