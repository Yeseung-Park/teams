from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_table, get_current_admin
from app.auth.schemas import TokenPayload
from app.order.schemas import OrderItemCreate, OrderResponse, OrderStatusUpdate, TableOrderSummary
from app.order.service import OrderService
from app.table.service import TableService
from app.sse.service import sse_service
import json

router = APIRouter(tags=["order"])
order_service = OrderService()
table_service = TableService()


@router.post("/customer/orders", response_model=OrderResponse)
async def create_order(items: list[OrderItemCreate], db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_table)):
    session_id = await table_service.ensure_session(db, user.table_id)
    return await order_service.create_order(db, user.store_id, user.table_id, session_id, items)


@router.get("/customer/orders", response_model=list[OrderResponse])
async def get_customer_orders(db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_table)):
    session_id = await table_service.ensure_session(db, user.table_id)
    return await order_service.get_orders_by_session(db, session_id)


@router.get("/admin/orders/stream")
async def stream_orders(db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    async def event_generator():
        queue = sse_service.connect(user.store_id)
        try:
            while True:
                event = await queue.get()
                yield f"event: {event['event']}\ndata: {json.dumps(event['data'])}\n\n"
        finally:
            sse_service.disconnect(user.store_id, queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/admin/orders", response_model=list[TableOrderSummary])
async def get_active_orders(db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    return await order_service.get_active_orders(db, user.store_id)


@router.patch("/admin/orders/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: int, data: OrderStatusUpdate, db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    return await order_service.update_order_status(db, user.store_id, order_id, data.status)


@router.delete("/admin/orders/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    await order_service.delete_order(db, user.store_id, order_id)
    return {"message": "Order deleted"}
