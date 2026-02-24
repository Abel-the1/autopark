from pydantic import BaseModel


class DriverBase(BaseModel):
    full_name: str
    phone: str | None = None
    telegram_id: int | None = None


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    telegram_id: int | None = None


class DriverOut(DriverBase):
    id: int

    model_config = {"from_attributes": True}
