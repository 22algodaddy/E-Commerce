from pydantic import BaseModel
from uuid import UUID

class PaymentRequest(BaseModel):
    order_id: UUID
    amount: float

class PaymentResponse(BaseModel):
    order_id: UUID
    status: str