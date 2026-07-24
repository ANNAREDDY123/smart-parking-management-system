from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.parking_lot import ParkingLot
from models.user import User
from models.vehicle_entry import VehicleEntry
from schemas.vehicle_entry import VehicleEntryCreate
from services.parking_service import (
    allocate_next_slot,
    calculate_parking_fee,
    valid_entry_exit_time,
    valid_vehicle_number
)

router = APIRouter(
    prefix="/entries",
    tags=["Vehicle Entries"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_entry(
    entry: VehicleEntryCreate,
    db: Session = Depends(get_db)
):

    customer = db.query(User).filter(
        User.id == entry.customer_id
    ).first()

    if not customer:

        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    parking = db.query(ParkingLot).filter(
        ParkingLot.id == entry.parking_id
    ).first()

    if not parking:

        raise HTTPException(
            status_code=404,
            detail="Parking lot not found."
        )

    if parking.available_slots <= 0:

        raise HTTPException(
            status_code=400,
            detail="Parking lot is full."
        )

    existing = db.query(VehicleEntry).filter(
        VehicleEntry.vehicle_number == entry.vehicle_number,
        VehicleEntry.exit_time == None
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Vehicle is already parked."
        )

    if not valid_vehicle_number(entry.vehicle_number):

        raise HTTPException(
            status_code=400,
            detail="Invalid vehicle number."
        )

    slot = allocate_next_slot(
        parking.available_slots,
        parking.total_slots
    )

    db_entry = VehicleEntry(
        customer_id=entry.customer_id,
        parking_id=entry.parking_id,
        vehicle_number=entry.vehicle_number,
        vehicle_type=entry.vehicle_type,
        entry_time=entry.entry_time,
        slot_number=slot,
        parking_fee=0
    )

    parking.available_slots -= 1

    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return db_entry


@router.get("/")
def get_entries(
    vehicle_number: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(VehicleEntry)

    if vehicle_number:
        query = query.filter(
            VehicleEntry.vehicle_number.contains(vehicle_number)
        )

    total = query.count()

    entries = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": entries
    }


@router.get("/{entry_id}")
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):

    entry = db.query(VehicleEntry).filter(
        VehicleEntry.id == entry_id
    ).first()

    if not entry:

        raise HTTPException(
            status_code=404,
            detail="Entry not found."
        )

    return entry


@router.put("/{entry_id}")
def update_entry(
    entry_id: int,
    entry: VehicleEntryCreate,
    db: Session = Depends(get_db)
):

    db_entry = db.query(VehicleEntry).filter(
        VehicleEntry.id == entry_id
    ).first()

    if not db_entry:

        raise HTTPException(
            status_code=404,
            detail="Entry not found."
        )

    if not valid_entry_exit_time(
        db_entry.entry_time,
        entry.exit_time
    ):

        raise HTTPException(
            status_code=400,
            detail="Exit time must be after entry time."
        )

    parking = db.query(ParkingLot).filter(
        ParkingLot.id == db_entry.parking_id
    ).first()

    parking.available_slots += 1

    fee = calculate_parking_fee(
        db_entry.entry_time,
        entry.exit_time
    )

    db_entry.exit_time = entry.exit_time
    db_entry.parking_fee = fee

    db.commit()
    db.refresh(db_entry)

    return db_entry
