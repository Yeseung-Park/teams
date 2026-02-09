from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.auth.schemas import TokenPayload
from app.order.schemas import OrderResponse
from app.table.service import TableService

router = APIRouter(prefix="/admin/tables", tags=["table"])
table_service = TableService()


@router.post("/{table_id}/complete")
async def complete_table(table_id: int, db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    await table_service.complete_table(db, user.store_id, table_id)
    return {"message": "Table completed"}


@router.get("/{table_id}/history", response_model=list[OrderResponse])
async def get_table_history(table_id: int, date_from: date | None = Query(None), db: AsyncSession = Depends(get_db), user: TokenPayload = Depends(get_current_admin)):
    return await table_service.get_table_history(db, user.store_id, table_id, date_from)
