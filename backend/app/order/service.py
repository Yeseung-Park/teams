from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.order.schemas import OrderItemCreate, OrderResponse, TableOrderSummary, OrderItemResponse
from app.models.models import Menu, Order, OrderItem, Table, TableSession
from app.sse.service import sse_service

VALID_TRANSITIONS = {
    "pending": ["preparing"],
    "preparing": ["completed"],
    "completed": []
}


class OrderService:
    def _generate_order_number(self) -> str:
        return datetime.now().strftime("%Y%m%d") + "-" + str(int(datetime.now().timestamp()) % 10000).zfill(4)

    async def create_order(self, db: AsyncSession, store_id: int, table_id: int, session_id: int, items: list[OrderItemCreate]) -> OrderResponse:
        if not items:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must have at least one item")
        
        order_items = []
        total = 0
        
        for item in items:
            result = await db.execute(select(Menu).where(Menu.menu_id == item.menu_id))
            menu = result.scalar_one_or_none()
            
            if not menu or menu.store_id != store_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Menu {item.menu_id} not found")
            if not menu.is_available:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Menu {menu.menu_name} is not available")
            
            subtotal = menu.price * item.quantity
            total += subtotal
            order_items.append(OrderItem(
                menu_id=menu.menu_id,
                menu_name=menu.menu_name,
                quantity=item.quantity,
                unit_price=menu.price,
                subtotal=subtotal
            ))
        
        order = Order(
            store_id=store_id,
            table_id=table_id,
            session_id=session_id,
            order_number=self._generate_order_number(),
            total_amount=total,
            order_status="pending"
        )
        order.items = order_items
        
        db.add(order)
        await db.commit()
        await db.refresh(order, ["items"])
        
        await sse_service.broadcast(store_id, "new_order", {"order_id": order.order_id, "table_id": table_id})
        
        return OrderResponse(
            order_id=order.order_id,
            order_number=order.order_number,
            total_amount=order.total_amount,
            order_status=order.order_status,
            created_at=order.created_at,
            items=[OrderItemResponse.model_validate(i) for i in order.items]
        )

    async def get_orders_by_session(self, db: AsyncSession, session_id: int) -> list[OrderResponse]:
        result = await db.execute(
            select(Order)
            .where(Order.session_id == session_id)
            .options(selectinload(Order.items))
            .order_by(Order.created_at.desc())
        )
        orders = result.scalars().all()
        return [OrderResponse.model_validate(o) for o in orders]

    async def get_active_orders(self, db: AsyncSession, store_id: int) -> list[TableOrderSummary]:
        result = await db.execute(
            select(Table)
            .where(Table.store_id == store_id, Table.current_session_id.isnot(None))
        )
        tables = result.scalars().all()
        
        summaries = []
        for table in tables:
            orders = await self.get_orders_by_session(db, table.current_session_id)
            total = sum(o.total_amount for o in orders)
            summaries.append(TableOrderSummary(
                table_id=table.table_id,
                table_number=table.table_number,
                total_amount=total,
                orders=orders
            ))
        return summaries

    async def update_order_status(self, db: AsyncSession, store_id: int, order_id: int, new_status: str) -> OrderResponse:
        result = await db.execute(
            select(Order)
            .where(Order.order_id == order_id, Order.store_id == store_id)
            .options(selectinload(Order.items))
        )
        order = result.scalar_one_or_none()
        
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        if new_status not in VALID_TRANSITIONS.get(order.order_status, []):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid status transition from {order.order_status} to {new_status}")
        
        order.order_status = new_status
        await db.commit()
        await db.refresh(order)
        
        await sse_service.broadcast(store_id, "order_updated", {"order_id": order_id, "status": new_status})
        
        return OrderResponse.model_validate(order)

    async def delete_order(self, db: AsyncSession, store_id: int, order_id: int) -> None:
        result = await db.execute(select(Order).where(Order.order_id == order_id, Order.store_id == store_id))
        order = result.scalar_one_or_none()
        
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
        
        await db.delete(order)
        await db.commit()
        
        await sse_service.broadcast(store_id, "order_deleted", {"order_id": order_id})
