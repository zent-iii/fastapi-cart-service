from typing import Optional

from pydantic import BaseModel, EmailStr, Field, PositiveInt, PositiveFloat

ShopName='Webshop'

class User(BaseModel):
    id: Optional[PositiveInt] = None
    name: str
    email: str
    class Config:
        from_attributes = True

class Item(BaseModel):
    item_id: PositiveInt = Field(alias='id')
    name: str
    brand: str
    price: PositiveFloat
    quantity: PositiveInt
    class Config:
        from_attributes = True
        populate_by_name = True


class Basket(BaseModel):
    id: PositiveInt
    user_id: PositiveInt
    items: list[Item] = []
    class Config:
        from_attributes = True