# smart-parking-management-system
A FastAPI-based Smart Parking Management System with JWT Authentication, Role-Based Authorization, Parking Lot Management, Vehicle Entry &amp; Exit, Payment Management, Automatic Slot Allocation, Parking Fee Calculation, Reports, Search, Pagination, SQLAlchemy ORM, Swagger Documentation, and Docker support.
# Smart Parking Management System

## Features

- JWT Authentication
- Role-Based Authorization
- Parking Lot Management
- Vehicle Entry & Exit
- Payment Management
- Automatic Slot Allocation
- Automatic Parking Fee Calculation
- Daily Revenue Report
- Search
- Filter
- Pagination

## Installation

pip install -r requirements.txt


Run


uvicorn main:app --reload


Swagger


http://127.0.0.1:8000/docs


## Roles

- Admin
- Parking Manager
- Customer

## Business Rules

- Unique vehicle while parked
- Automatic slot allocation
- Automatic slot release
- Duplicate payment prevention
- Entry time before exit time
