from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.parking_lot import ParkingLot
from schemas.parking_lot import ParkingLotCreate
from services.parking_service import valid_parking_status

router = APIRouter(
    prefix="/parking-lots",
    tags=["Parking Lots"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_parking_lot(
    parking: ParkingLotCreate,
    db: Session = Depends(get_db)
):

    if not valid_parking_status(parking.status):

        raise HTTPException(
            status_code=400,
            detail="Invalid parking status."
        )

    db_parking = ParkingLot(**parking.dict())

    db.add(db_parking)
    db.commit()
    db.refresh(db_parking)

    return db_parking


@router.get("/")
def get_parking_lots(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(ParkingLot)

    total = query.count()

    parking_lots = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": parking_lots
    }


@router.get("/{parking_id}")
def get_parking_lot(
    parking_id: int,
    db: Session = Depends(get_db)
):

    parking = db.query(ParkingLot).filter(
        ParkingLot.id == parking_id
    ).first()

    if not parking:

        raise HTTPException(
            status_code=404,
            detail="Parking lot not found."
        )

    return parking


@router.put("/{parking_id}")
def update_parking_lot(
    parking_id: int,
    parking: ParkingLotCreate,
    db: Session = Depends(get_db)
):

    db_parking = db.query(ParkingLot).filter(
        ParkingLot.id == parking_id
    ).first()

    if not db_parking:

        raise HTTPException(
            status_code=404,
            detail="Parking lot not found."
        )

    for key, value in parking.dict().items():
        setattr(db_parking, key, value)

    db.commit()
    db.refresh(db_parking)

    return db_parking


@router.delete("/{parking_id}")
def delete_parking_lot(
    parking_id: int,
    db: Session = Depends(get_db)
):

    parking = db.query(ParkingLot).filter(
        ParkingLot.id == parking_id
    ).first()

    if not parking:

        raise HTTPException(
            status_code=404,
            detail="Parking lot not found."
        )

    db.delete(parking)
    db.commit()

    return {
        "message": "Parking lot deleted successfully."
    }
