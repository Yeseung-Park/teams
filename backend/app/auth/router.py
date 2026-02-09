from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.auth.schemas import TableLoginRequest, AdminLoginRequest, TokenResponse
from app.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])
auth_service = AuthService()


@router.post("/customer/login", response_model=TokenResponse)
async def login_table(request: TableLoginRequest, db: AsyncSession = Depends(get_db)):
    return await auth_service.login_table(db, request.store_identifier, request.table_number, request.password)


@router.post("/admin/login", response_model=TokenResponse)
async def login_admin(request: AdminLoginRequest, db: AsyncSession = Depends(get_db)):
    return await auth_service.login_admin(db, request.store_identifier, request.username, request.password)
