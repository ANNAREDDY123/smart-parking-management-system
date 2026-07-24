from fastapi import FastAPI

from database import Base, engine

from routes.auth import router as auth_router
from routes.parking_lots import router as parking_router
from routes.entries import router as entry_router
from routes.payments import router as payment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Parking Management System"
)

app.include_router(auth_router)
app.include_router(parking_router)
app.include_router(entry_router)
app.include_router(payment_router)


@app.get("/")
def home():
    return {
        "message": "Smart Parking Management System API"
    }
