from typing import Optional, List
from pydantic import BaseModel, Field


class MenuCreate(BaseModel):
    category_id: int
    menu_name: str = Field(max_length=100)
    price: int = Field(gt=0)
    description: Optional[str] = None
    image_url: Optional[str] = None


class MenuUpdate(BaseModel):
    category_id: Optional[int] = None
    menu_name: Optional[str] = Field(default=None, max_length=100)
    price: Optional[int] = Field(default=None, gt=0)
    description: Optional[str] = None
    image_url: Optional[str] = None


class MenuOrderUpdate(BaseModel):
    menu_id: int
    display_order: int


class MenuResponse(BaseModel):
    menu_id: int
    category_id: int
    menu_name: str
    price: int
    description: Optional[str]
    image_url: Optional[str]
    display_order: int
    is_available: bool

    class Config:
        from_attributes = True


class CategoryWithMenus(BaseModel):
    category_id: int
    category_name: str
    menus: List[MenuResponse]

    class Config:
        from_attributes = True
