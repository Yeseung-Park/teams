import pytest
from datetime import datetime
from unittest.mock import MagicMock, AsyncMock, patch
from app.order.service import OrderService
from app.order.schemas import OrderItemCreate
from fastapi import HTTPException


@pytest.fixture
def order_service():
    return OrderService()


@pytest.fixture
def mock_db():
    return AsyncMock()


# TC-ORDER-001: 유효한 항목으로 주문 생성
@pytest.mark.asyncio
async def test_create_order_with_valid_items(order_service, mock_db):
    from app.models.models import Menu
    
    mock_menu = MagicMock(spec=Menu)
    mock_menu.menu_id = 1
    mock_menu.menu_name = "Test Menu"
    mock_menu.price = 10000
    mock_menu.is_available = True
    mock_menu.store_id = 1
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_menu
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    
    def mock_refresh(obj):
        if hasattr(obj, 'order_id'):
            obj.order_id = 1
            obj.order_number = "20260209-0001"
            obj.total_amount = 20000
            obj.order_status = "pending"
            obj.created_at = datetime.now()
            # Mock items
            mock_item = MagicMock()
            mock_item.order_item_id = 1
            mock_item.menu_id = 1
            mock_item.menu_name = "Test Menu"
            mock_item.quantity = 2
            mock_item.unit_price = 10000
            mock_item.subtotal = 20000
            obj.items = [mock_item]
    
    mock_db.refresh = AsyncMock(side_effect=mock_refresh)
    
    items = [OrderItemCreate(menu_id=1, quantity=2)]
    
    with patch('app.order.service.sse_service') as mock_sse:
        mock_sse.broadcast = AsyncMock()
        result = await order_service.create_order(mock_db, 1, 1, 1, items)
    
    assert result.order_id == 1
    assert result.total_amount == 20000


# TC-ORDER-002: 품절 메뉴로 주문 실패
@pytest.mark.asyncio
async def test_create_order_with_unavailable_menu(order_service, mock_db):
    from app.models.models import Menu
    
    mock_menu = MagicMock(spec=Menu)
    mock_menu.menu_id = 1
    mock_menu.is_available = False
    mock_menu.store_id = 1
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_menu
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    items = [OrderItemCreate(menu_id=1, quantity=1)]
    
    with pytest.raises(HTTPException) as exc_info:
        await order_service.create_order(mock_db, 1, 1, 1, items)
    
    assert exc_info.value.status_code == 400


# TC-ORDER-003: 빈 항목으로 주문 실패
@pytest.mark.asyncio
async def test_create_order_with_empty_items(order_service, mock_db):
    with pytest.raises(HTTPException) as exc_info:
        await order_service.create_order(mock_db, 1, 1, 1, [])
    
    assert exc_info.value.status_code == 400


# TC-ORDER-004: 세션별 주문 조회
@pytest.mark.asyncio
async def test_get_orders_by_session(order_service, mock_db):
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
    mock_order.order_status = "pending"
    mock_order.created_at = datetime.now()
    mock_order.items = [mock_item]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_order]
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    result = await order_service.get_orders_by_session(mock_db, 1)
    
    assert len(result) == 1
    assert result[0].order_id == 1


# TC-ORDER-005: 유효한 상태 전환
@pytest.mark.asyncio
async def test_update_order_status_valid_transition(order_service, mock_db):
    from app.models.models import Order
    
    mock_order = MagicMock(spec=Order)
    mock_order.order_id = 1
    mock_order.store_id = 1
    mock_order.order_status = "pending"
    mock_order.order_number = "20260209-0001"
    mock_order.total_amount = 10000
    mock_order.created_at = datetime.now()
    mock_order.items = []
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_order
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    with patch('app.order.service.sse_service') as mock_sse:
        mock_sse.broadcast = AsyncMock()
        result = await order_service.update_order_status(mock_db, 1, 1, "preparing")
    
    assert mock_order.order_status == "preparing"


# TC-ORDER-006: 잘못된 상태 전환
@pytest.mark.asyncio
async def test_update_order_status_invalid_transition(order_service, mock_db):
    from app.models.models import Order
    
    mock_order = MagicMock(spec=Order)
    mock_order.order_id = 1
    mock_order.store_id = 1
    mock_order.order_status = "completed"
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_order
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    with pytest.raises(HTTPException) as exc_info:
        await order_service.update_order_status(mock_db, 1, 1, "pending")
    
    assert exc_info.value.status_code == 400


# TC-ORDER-007: 주문 삭제
@pytest.mark.asyncio
async def test_delete_order(order_service, mock_db):
    from app.models.models import Order
    
    mock_order = MagicMock(spec=Order)
    mock_order.order_id = 1
    mock_order.store_id = 1
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_order
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.delete = AsyncMock()
    mock_db.commit = AsyncMock()
    
    await order_service.delete_order(mock_db, 1, 1)
    
    mock_db.delete.assert_called_once_with(mock_order)
