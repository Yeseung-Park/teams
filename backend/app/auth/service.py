from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.auth.schemas import TokenResponse, TokenPayload
from app.models.models import Store, Table
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def _create_token(self, store_id: int, table_id: Optional[int] = None, is_admin: bool = False) -> str:
        expire = datetime.utcnow() + timedelta(hours=settings.jwt_expire_hours)
        payload = {"store_id": store_id, "table_id": table_id, "is_admin": is_admin, "exp": expire}
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    async def login_table(self, db: AsyncSession, store_identifier: str, table_number: int, password: str) -> TokenResponse:
        # Find store
        result = await db.execute(select(Store).where(Store.store_identifier == store_identifier))
        store = result.scalar_one_or_none()
        if not store:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Find table
        result = await db.execute(select(Table).where(Table.store_id == store.store_id, Table.table_number == table_number))
        table = result.scalar_one_or_none()
        if not table:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Verify password
        if not pwd_context.verify(password, table.table_password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        token = self._create_token(store.store_id, table.table_id, is_admin=False)
        return TokenResponse(access_token=token)

    async def login_admin(self, db: AsyncSession, store_identifier: str, username: str, password: str) -> TokenResponse:
        # Find store
        result = await db.execute(select(Store).where(Store.store_identifier == store_identifier, Store.admin_username == username))
        store = result.scalar_one_or_none()
        if not store:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        # Verify password
        if not pwd_context.verify(password, store.admin_password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        
        token = self._create_token(store.store_id, is_admin=True)
        return TokenResponse(access_token=token)

    def verify_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
            return TokenPayload(store_id=payload["store_id"], table_id=payload.get("table_id"), is_admin=payload.get("is_admin", False))
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
