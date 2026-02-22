from pydantic import BaseModel
from uuid import UUID

class OrderCreate(BaseModel):
    user_id: str
    product_id: str

class OrderResponse(BaseModel):
    id: UUID
    user_id: str
    product_id: str
    status: str
    total_amount: float

    class Config:
        from_attributes = True