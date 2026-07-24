from pydantic import BaseModel
from pydantic import Field


class ParkingLotCreate(BaseModel):

    parking_name: str = Field(..., min_length=3, max_length=100)

    location: str = Field(..., min_length=3, max_length=150)

    total_slots: int = Field(..., gt=0)

    available_slots: int = Field(..., ge=0)

    status: str


class ParkingLotResponse(ParkingLotCreate):

    id: int

    class Config:
        from_attributes = True
