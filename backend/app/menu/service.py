from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.menu.schemas import MenuCreate, MenuUpdate, MenuResponse, MenuOrderUpdate, CategoryWithMenus
from app.models.models import Category, Menu


class MenuService:
    async def get_menus(self, db: AsyncSession, store_id: int) -> list[CategoryWithMenus]:
        result = await db.execute(
            select(Category)
            .where(Category.store_id == store_id)
            .options(selectinload(Category.menus))
            .order_by(Category.display_order)
        )
        categories = result.scalars().all()
        
        return [
            CategoryWithMenus(
                category_id=cat.category_id,
                category_name=cat.category_name,
                menus=[MenuResponse.model_validate(m) for m in cat.menus if m.is_available]
            )
            for cat in categories
        ]

    async def create_menu(self, db: AsyncSession, store_id: int, data: MenuCreate) -> MenuResponse:
        menu = Menu(
            store_id=store_id,
            category_id=data.category_id,
            menu_name=data.menu_name,
            price=data.price,
            description=data.description,
            image_url=data.image_url
        )
        db.add(menu)
        await db.commit()
        await db.refresh(menu)
        return MenuResponse.model_validate(menu)

    async def update_menu(self, db: AsyncSession, store_id: int, menu_id: int, data: MenuUpdate) -> MenuResponse:
        result = await db.execute(select(Menu).where(Menu.menu_id == menu_id, Menu.store_id == store_id))
        menu = result.scalar_one_or_none()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(menu, field, value)
        
        await db.commit()
        await db.refresh(menu)
        return MenuResponse.model_validate(menu)

    async def delete_menu(self, db: AsyncSession, store_id: int, menu_id: int) -> None:
        result = await db.execute(select(Menu).where(Menu.menu_id == menu_id, Menu.store_id == store_id))
        menu = result.scalar_one_or_none()
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        
        menu.is_available = False
        await db.commit()

    async def update_menu_order(self, db: AsyncSession, store_id: int, orders: list[MenuOrderUpdate]) -> None:
        for order in orders:
            result = await db.execute(select(Menu).where(Menu.menu_id == order.menu_id, Menu.store_id == store_id))
            menu = result.scalar_one_or_none()
            if menu:
                menu.display_order = order.display_order
        await db.commit()
