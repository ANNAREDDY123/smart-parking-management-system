from pydantic import BaseModel
from pydantic import Field


class PaymentCreate(BaseModel):

    entry_id: int

    amount: float = Field(..., gt=0)

    payment_method: str

    payment_status: str


class PaymentResponse(PaymentCreate):

    id: int

    class Config:
        from_attributes = True
