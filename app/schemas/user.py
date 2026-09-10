from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    dob: date
    phone: str
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    name: str
    email: EmailStr
    dob: date
    phone: str
    create_date: datetime


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    dob: date | None = None
    phone: str | None = None