from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_table, get_current_admin
from app.auth.schemas import TokenPayload
from app.menu.schemas import MenuCreate, MenuUpdate, MenuResponse, MenuOrderUpdate, CategoryWithMenus
from app.menu.service import MenuService

router = APIRouter(tags=["menu"])
menu_service = MenuService()


@router.get("/customer/menus", response_model=list[CategoryWithMenus])
async def get_customer_menus(db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_table)):
    return await menu_service.get_menus(db, user.store_id)


@router.get("/admin/menus", response_model=list[CategoryWithMenus])
async def get_admin_menus(db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    return await menu_service.get_menus(db, user.store_id)


@router.post("/admin/menus", response_model=MenuResponse)
async def create_menu(data: MenuCreate, db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    return await menu_service.create_menu(db, user.store_id, data)


@router.put("/admin/menus/{menu_id}", response_model=MenuResponse)
async def update_menu(menu_id: int, data: MenuUpdate, db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    return await menu_service.update_menu(db, user.store_id, menu_id, data)


@router.delete("/admin/menus/{menu_id}")
async def delete_menu(menu_id: int, db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    await menu_service.delete_menu(db, user.store_id, menu_id)
    return {"message": "Menu deleted"}


@router.patch("/admin/menus/order")
async def update_menu_order(orders: list[MenuOrderUpdate], db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    await menu_service.update_menu_order(db, user.store_id, orders)
    return {"message": "Order updated"}
