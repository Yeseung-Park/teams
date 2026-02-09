import pytest
from unittest.mock import MagicMock, AsyncMock, PropertyMock
from app.menu.service import MenuService
from app.menu.schemas import MenuCreate, MenuUpdate
from fastapi import HTTPException


@pytest.fixture
def menu_service():
    return MenuService()


@pytest.fixture
def mock_db():
    return AsyncMock()


# TC-MENU-001: 메뉴 목록 조회
@pytest.mark.asyncio
async def test_get_menus(menu_service, mock_db):
    from app.models.models import Category, Menu
    
    mock_menu = MagicMock()
    mock_menu.menu_id = 1
    mock_menu.category_id = 1
    mock_menu.menu_name = "Test Menu"
    mock_menu.price = 10000
    mock_menu.description = "Test"
    mock_menu.image_url = None
    mock_menu.display_order = 0
    mock_menu.is_available = True
    
    mock_category = MagicMock()
    mock_category.category_id = 1
    mock_category.category_name = "Main"
    mock_category.menus = [mock_menu]
    
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_category]
    mock_db.execute = AsyncMock(return_value=mock_result)
    
    result = await menu_service.get_menus(mock_db, 1)
    
    assert len(result) == 1
    assert result[0].category_name == "Main"


# TC-MENU-002: 메뉴 생성
@pytest.mark.asyncio
async def test_create_menu_with_valid_data(menu_service, mock_db):
    data = MenuCreate(category_id=1, menu_name="New Menu", price=15000)
    
    mock_menu = MagicMock()
    mock_menu.menu_id = 1
    mock_menu.category_id = 1
    mock_menu.menu_name = "New Menu"
    mock_menu.price = 15000
    mock_menu.description = None
    mock_menu.image_url = None
    mock_menu.display_order = 0
    mock_menu.is_available = True
    
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock(side_effect=lambda m: setattr(m, 'menu_id', 1) or setattr(m, 'display_order', 0) or setattr(m, 'is_available', True))
    
    result = await menu_service.create_menu(mock_db, 1, data)
    
    assert result.menu_name == "New Menu"
    assert result.price == 15000


# TC-MENU-003: 잘못된 가격으로 메뉴 생성 실패
@pytest.mark.asyncio
async def test_create_menu_with_invalid_price(menu_service, mock_db):
    from pydantic import ValidationError
    
    with pytest.raises(ValidationError):
        MenuCreate(category_id=1, menu_name="Test", price=-100)


# TC-MENU-004: 메뉴 수정
@pytest.mark.asyncio
async def test_update_menu(menu_service, mock_db):
    from app.models.models import Menu
    
    mock_menu = MagicMock(spec=Menu)
    mock_menu.menu_id = 1
    mock_menu.store_id = 1
    mock_menu.category_id = 1
    mock_menu.menu_name = "Old Name"
    mock_menu.price = 10000
    mock_menu.description = None
    mock_menu.image_url = None
    mock_menu.display_order = 0
    mock_menu.is_available = True
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_menu
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    data = MenuUpdate(menu_name="New Name")
    result = await menu_service.update_menu(mock_db, 1, 1, data)
    
    assert mock_menu.menu_name == "New Name"


# TC-MENU-005: 메뉴 삭제 (soft delete)
@pytest.mark.asyncio
async def test_delete_menu(menu_service, mock_db):
    from app.models.models import Menu
    
    mock_menu = MagicMock(spec=Menu)
    mock_menu.menu_id = 1
    mock_menu.store_id = 1
    mock_menu.is_available = True
    
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_menu
    mock_db.execute = AsyncMock(return_value=mock_result)
    mock_db.commit = AsyncMock()
    
    await menu_service.delete_menu(mock_db, 1, 1)
    
    assert mock_menu.is_available == False
