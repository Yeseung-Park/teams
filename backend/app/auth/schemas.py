from typing import Optional
from pydantic import BaseModel


class TableLoginRequest(BaseModel):
    store_identifier: str
    table_number: int
    password: str


class AdminLoginRequest(BaseModel):
    store_identifier: str
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    store_id: int
    table_id: Optional[int] = None
    is_admin: bool = False
