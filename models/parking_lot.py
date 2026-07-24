from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class ParkingLot(Base):

    __tablename__ = "parking_lots"

    id = Column(Integer, primary_key=True, index=True)

    parking_name = Column(String(100), nullable=False)

    location = Column(String(150), nullable=False)

    total_slots = Column(Integer, nullable=False)

    available_slots = Column(Integer, nullable=False)

    status = Column(String(20), nullable=False)
