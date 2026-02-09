from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.service import AuthService
from app.auth.schemas import TokenPayload

security = HTTPBearer()
auth_service = AuthService()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenPayload:
    return auth_service.verify_token(credentials.credentials)


async def get_current_admin(user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


async def get_current_table(user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
    if user.is_admin or user.table_id is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Table access required")
    return user
