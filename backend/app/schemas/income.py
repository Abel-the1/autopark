from pydantic import BaseModel
import datetime


class IncomeCreate(BaseModel):
    car_id: int
    driver_id: int | None = None
    amount: float
    date: datetime.date
    description: str | None = None
    payment_type: str | None = None
    created_by: str | None = None


class IncomeUpdate(BaseModel):
    car_id: int | None = None
    driver_id: int | None = None
    amount: float | None = None
    date: datetime.date | None = None
    description: str | None = None
    payment_type: str | None = None


class CarShort(BaseModel):
    id: int
    name: str
    plate_number: str
    model_config = {"from_attributes": True}


class DriverShort(BaseModel):
    id: int
    full_name: str
    model_config = {"from_attributes": True}


class IncomeOut(BaseModel):
    id: int
    car_id: int
    driver_id: int | None
    amount: float
    date: datetime.date
    description: str | None
    payment_type: str | None
    created_by: str | None
    created_at: datetime.datetime
    car: CarShort | None = None
    driver: DriverShort | None = None

    model_config = {"from_attributes": True}
