from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    menu_id: int
    quantity: int = Field(ge=1, le=99)


class OrderItemResponse(BaseModel):
    order_item_id: int
    menu_id: int
    menu_name: str
    quantity: int
    unit_price: int
    subtotal: int

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    order_id: int
    order_number: str
    total_amount: int
    order_status: str
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: str


class TableOrderSummary(BaseModel):
    table_id: int
    table_number: int
    total_amount: int
    orders: List[OrderResponse]
