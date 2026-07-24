from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class UserCreate(BaseModel):

    username: str = Field(..., min_length=3, max_length=100)

    email: EmailStr

    password: str = Field(..., min_length=6)

    role: str


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class UserResponse(BaseModel):

    id: int

    username: str

    email: EmailStr

    role: str

    class Config:
        from_attributes = True
