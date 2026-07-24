from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.payment import Payment
from models.vehicle_entry import VehicleEntry
from schemas.payment import PaymentCreate
from services.parking_service import (
    duplicate_payment_exists,
    valid_payment_status
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):

    entry = db.query(VehicleEntry).filter(
        VehicleEntry.id == payment.entry_id
    ).first()

    if not entry:

        raise HTTPException(
            status_code=404,
            detail="Parking entry not found."
        )

    existing = db.query(Payment).filter(
        Payment.entry_id == payment.entry_id
    ).first()

    if duplicate_payment_exists(existing):

        raise HTTPException(
            status_code=400,
            detail="Payment already exists for this parking entry."
        )

    if not valid_payment_status(payment.payment_status):

        raise HTTPException(
            status_code=400,
            detail="Invalid payment status."
        )

    db_payment = Payment(
        entry_id=payment.entry_id,
        amount=entry.parking_fee,
        payment_method=payment.payment_method,
        payment_status=payment.payment_status
    )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment


@router.get("/")
def get_payments(
    payment_status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Payment)

    if payment_status:
        query = query.filter(
            Payment.payment_status == payment_status
        )

    total = query.count()

    payments = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": payments
    }


@router.get("/{payment_id}")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    payment = db.query(Payment).filter(
        Payment.id == payment_id
    ).first()

    if not payment:

        raise HTTPException(
            status_code=404,
            detail="Payment not found."
        )

    return payment


@router.get("/reports/daily-revenue")
def daily_revenue(
    db: Session = Depends(get_db)
):

    payments = db.query(Payment).filter(
        Payment.payment_status == "Paid"
    ).all()

    revenue = sum(
        payment.amount
        for payment in payments
    )

    return {
        "daily_revenue": revenue
    }


@router.get("/reports/filter")
def filter_payments(
    payment_status: str = None,
    parking_date: str = None,
    db: Session = Depends(get_db)
):

    query = db.query(Payment).join(
        VehicleEntry,
        Payment.entry_id == VehicleEntry.id
    )

    if payment_status:
        query = query.filter(
            Payment.payment_status == payment_status
        )

    if parking_date:
        query = query.filter(
            VehicleEntry.entry_time.startswith(parking_date)
        )

    return query.all()
