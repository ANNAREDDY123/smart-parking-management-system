from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Payment(Base):

    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    entry_id = Column(
        Integer,
        ForeignKey("vehicle_entries.id"),
        unique=True,
        nullable=False
    )

    amount = Column(Float, nullable=False)

    payment_method = Column(String(50), nullable=False)

    payment_status = Column(String(20), nullable=False)
