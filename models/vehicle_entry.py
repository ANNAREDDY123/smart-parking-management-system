from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class VehicleEntry(Base):

    __tablename__ = "vehicle_entries"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    parking_id = Column(
        Integer,
        ForeignKey("parking_lots.id"),
        nullable=False
    )

    vehicle_number = Column(
        String(30),
        unique=True,
        nullable=False
    )

    vehicle_type = Column(String(30), nullable=False)

    entry_time = Column(DateTime, nullable=False)

    exit_time = Column(DateTime, nullable=True)

    slot_number = Column(Integer, nullable=False)

    parking_fee = Column(
        Float,
        default=0
    )
