from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, case
from app.database import get_db
from app.models import Expense, Income, Car, Driver
import datetime

router = APIRouter()


@router.get("/summary")
async def summary(
    date_from: datetime.date | None = Query(None),
    date_to: datetime.date | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Общая сводка: доходы, расходы, прибыль"""
    exp_q = select(func.coalesce(func.sum(Expense.amount), 0))
    inc_q = select(func.coalesce(func.sum(Income.amount), 0))

    if date_from:
        exp_q = exp_q.where(Expense.date >= date_from)
        inc_q = inc_q.where(Income.date >= date_from)
    if date_to:
        exp_q = exp_q.where(Expense.date <= date_to)
        inc_q = inc_q.where(Income.date <= date_to)

    total_expenses = (await db.execute(exp_q)).scalar()
    total_incomes = (await db.execute(inc_q)).scalar()

    return {
        "total_incomes": float(total_incomes),
        "total_expenses": float(total_expenses),
        "profit": float(total_incomes) - float(total_expenses),
    }


@router.get("/by-car")
async def by_car(
    date_from: datetime.date | None = Query(None),
    date_to: datetime.date | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Аналитика по машинам"""
    cars = (await db.execute(select(Car))).scalars().all()
    result = []
    for car in cars:
        exp_q = select(func.coalesce(func.sum(Expense.amount), 0)).where(Expense.car_id == car.id)
        inc_q = select(func.coalesce(func.sum(Income.amount), 0)).where(Income.car_id == car.id)
        if date_from:
            exp_q = exp_q.where(Expense.date >= date_from)
            inc_q = inc_q.where(Income.date >= date_from)
        if date_to:
            exp_q = exp_q.where(Expense.date <= date_to)
            inc_q = inc_q.where(Income.date <= date_to)
        exp = float((await db.execute(exp_q)).scalar())
        inc = float((await db.execute(inc_q)).scalar())
        result.append({
            "car_id": car.id,
            "car_name": car.name,
            "plate_number": car.plate_number,
            "total_incomes": inc,
            "total_expenses": exp,
            "profit": inc - exp,
        })
    return result


@router.get("/by-driver")
async def by_driver(
    date_from: datetime.date | None = Query(None),
    date_to: datetime.date | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Аналитика по водителям"""
    drivers = (await db.execute(select(Driver))).scalars().all()
    result = []
    for driver in drivers:
        exp_q = select(func.coalesce(func.sum(Expense.amount), 0)).where(Expense.driver_id == driver.id)
        inc_q = select(func.coalesce(func.sum(Income.amount), 0)).where(Income.driver_id == driver.id)
        if date_from:
            exp_q = exp_q.where(Expense.date >= date_from)
            inc_q = inc_q.where(Income.date >= date_from)
        if date_to:
            exp_q = exp_q.where(Expense.date <= date_to)
            inc_q = inc_q.where(Income.date <= date_to)
        exp = float((await db.execute(exp_q)).scalar())
        inc = float((await db.execute(inc_q)).scalar())
        result.append({
            "driver_id": driver.id,
            "driver_name": driver.full_name,
            "total_incomes": inc,
            "total_expenses": exp,
            "profit": inc - exp,
        })
    return result


@router.get("/by-month")
async def by_month(
    year: int = Query(default=2024),
    db: AsyncSession = Depends(get_db),
):
    """Помесячная аналитика за год"""
    result = []
    for month in range(1, 13):
        date_from = datetime.date(year, month, 1)
        if month == 12:
            date_to = datetime.date(year, 12, 31)
        else:
            date_to = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        exp = float((await db.execute(
            select(func.coalesce(func.sum(Expense.amount), 0))
            .where(Expense.date >= date_from)
            .where(Expense.date <= date_to)
        )).scalar())
        inc = float((await db.execute(
            select(func.coalesce(func.sum(Income.amount), 0))
            .where(Income.date >= date_from)
            .where(Income.date <= date_to)
        )).scalar())
        result.append({
            "month": month,
            "month_name": date_from.strftime("%B"),
            "total_incomes": inc,
            "total_expenses": exp,
            "profit": inc - exp,
        })
    return result
