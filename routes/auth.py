from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from sqlalchemy.orm import Session

from database import SessionLocal
from models.user import User
from schemas.user import UserCreate, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

SECRET_KEY = "smart_parking_secret_key"
ALGORITHM = "HS256"


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
        role=user.role
    )

    db.add(db_user)
    db.commit()

    return {
        "message": "User registered successfully."
    }


@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    if db_user.password != user.password:

        raise HTTPException(
            status_code=401,
            detail="Invalid password."
        )

    token = jwt.encode(
        {
            "sub": db_user.email,
            "role": db_user.role,
            "exp": datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }
