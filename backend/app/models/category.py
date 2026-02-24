from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")
