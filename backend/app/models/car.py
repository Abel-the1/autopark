from sqlalchemy import String, Integer, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
import enum


class CarStatus(str, enum.Enum):
    active = "active"
    idle = "idle"
    maintenance = "maintenance"
    archived = "archived"


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    plate_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[CarStatus] = mapped_column(
        SAEnum(CarStatus), default=CarStatus.active, nullable=False
    )

    expenses: Mapped[list["Expense"]] = relationship(back_populates="car")
    incomes: Mapped[list["Income"]] = relationship(back_populates="car")
