from sqlalchemy import String, Integer, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    telegram_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, unique=True)

    expenses: Mapped[list["Expense"]] = relationship(back_populates="driver")
    incomes: Mapped[list["Income"]] = relationship(back_populates="driver")
