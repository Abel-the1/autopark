from sqlalchemy import Integer, Numeric, Date, Text, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import Base
import datetime


class Income(Base):
    __tablename__ = "incomes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    car_id: Mapped[int] = mapped_column(ForeignKey("cars.id"), nullable=False, index=True)
    driver_id: Mapped[int | None] = mapped_column(ForeignKey("drivers.id"), nullable=True, index=True)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    payment_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    car: Mapped["Car"] = relationship(back_populates="incomes")
    driver: Mapped["Driver | None"] = relationship(back_populates="incomes")
