from datetime import datetime

from pydantic import BaseModel
from pydantic import Field


class VehicleEntryCreate(BaseModel):

    customer_id: int

    parking_id: int

    vehicle_number: str = Field(..., min_length=5, max_length=30)

    vehicle_type: str

    entry_time: datetime

    exit_time: datetime | None = None

    slot_number: int = 0

    parking_fee: float = 0


class VehicleEntryResponse(VehicleEntryCreate):

    id: int

    class Config:
        from_attributes = True
