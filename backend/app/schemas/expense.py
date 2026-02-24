from pydantic import BaseModel
import datetime


class ExpenseCreate(BaseModel):
    car_id: int
    driver_id: int | None = None
    category_id: int | None = None
    amount: float
    date: datetime.date
    description: str | None = None
    created_by: str | None = None


class ExpenseUpdate(BaseModel):
    car_id: int | None = None
    driver_id: int | None = None
    category_id: int | None = None
    amount: float | None = None
    date: datetime.date | None = None
    description: str | None = None


class CarShort(BaseModel):
    id: int
    name: str
    plate_number: str
    model_config = {"from_attributes": True}


class DriverShort(BaseModel):
    id: int
    full_name: str
    model_config = {"from_attributes": True}


class CategoryShort(BaseModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class ExpenseOut(BaseModel):
    id: int
    car_id: int
    driver_id: int | None
    category_id: int | None
    amount: float
    date: datetime.date
    description: str | None
    created_by: str | None
    created_at: datetime.datetime
    car: CarShort | None = None
    driver: DriverShort | None = None
    category: CategoryShort | None = None

    model_config = {"from_attributes": True}
