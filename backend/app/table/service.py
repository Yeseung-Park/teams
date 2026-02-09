from datetime import date, datetime
from typing import Optional, List
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.order.schemas import OrderResponse
from app.models.models import Table, TableSession, Order
from app.sse.service import sse_service


class TableService:
    async def ensure_session(self, db: AsyncSession, table_id: int) -> int:
        result = await db.execute(select(Table).where(Table.table_id == table_id))
        table = result.scalar_one_or_none()
        
        if not table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        
        if table.current_session_id:
            return table.current_session_id
        
        session = TableSession(table_id=table_id)
        db.add(session)
        await db.commit()
        await db.refresh(session)
        
        table.current_session_id = session.session_id
        await db.commit()
        
        return session.session_id

    async def complete_table(self, db: AsyncSession, store_id: int, table_id: int) -> None:
        result = await db.execute(select(Table).where(Table.table_id == table_id, Table.store_id == store_id))
        table = result.scalar_one_or_none()
        
        if not table:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Table not found")
        
        if not table.current_session_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No active session")
        
        result = await db.execute(select(TableSession).where(TableSession.session_id == table.current_session_id))
        session = result.scalar_one_or_none()
        
        if session:
            session.is_active = False
            session.session_end_time = datetime.utcnow()
        
        table.current_session_id = None
        await db.commit()
        
        await sse_service.broadcast(store_id, "table_reset", {"table_id": table_id})

    async def get_table_history(self, db: AsyncSession, store_id: int, table_id: int, date_from: Optional[date] = None) -> List[OrderResponse]:
        query = select(TableSession).where(
            TableSession.table_id == table_id,
            TableSession.is_active == False
        ).options(selectinload(TableSession.orders).selectinload(Order.items))
        
        if date_from:
            query = query.where(TableSession.session_end_time >= datetime.combine(date_from, datetime.min.time()))
        
        result = await db.execute(query.order_by(TableSession.session_end_time.desc()))
        sessions = result.scalars().all()
        
        orders = []
        for session in sessions:
            for order in session.orders:
                orders.append(OrderResponse.model_validate(order))
        
        return orders
