from pydantic import BaseModel
from app.models.car import CarStatus


class CarBase(BaseModel):
    name: str
    plate_number: str
    year: int | None = None
    status: CarStatus = CarStatus.active


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    name: str | None = None
    plate_number: str | None = None
    year: int | None = None
    status: CarStatus | None = None


class CarOut(CarBase):
    id: int

    model_config = {"from_attributes": True}
