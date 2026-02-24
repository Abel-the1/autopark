from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import Income
from app.schemas.income import IncomeCreate, IncomeUpdate, IncomeOut
import datetime

router = APIRouter()


@router.get("/", response_model=list[IncomeOut])
async def list_incomes(
    car_id: int | None = Query(None),
    driver_id: int | None = Query(None),
    date_from: datetime.date | None = Query(None),
    date_to: datetime.date | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    q = select(Income).options(
        selectinload(Income.car),
        selectinload(Income.driver),
    )
    if car_id:
        q = q.where(Income.car_id == car_id)
    if driver_id:
        q = q.where(Income.driver_id == driver_id)
    if date_from:
        q = q.where(Income.date >= date_from)
    if date_to:
        q = q.where(Income.date <= date_to)
    q = q.order_by(Income.date.desc())
    result = await db.execute(q)
    return result.scalars().all()


@router.post("/", response_model=IncomeOut, status_code=201)
async def create_income(data: IncomeCreate, db: AsyncSession = Depends(get_db)):
    income = Income(**data.model_dump())
    db.add(income)
    await db.commit()
    await db.refresh(income)
    return income


@router.get("/{income_id}", response_model=IncomeOut)
async def get_income(income_id: int, db: AsyncSession = Depends(get_db)):
    income = await db.get(Income, income_id)
    if not income:
        raise HTTPException(404, "Доход не найден")
    return income


@router.patch("/{income_id}", response_model=IncomeOut)
async def update_income(income_id: int, data: IncomeUpdate, db: AsyncSession = Depends(get_db)):
    income = await db.get(Income, income_id)
    if not income:
        raise HTTPException(404, "Доход не найден")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(income, field, value)
    await db.commit()
    await db.refresh(income)
    return income


@router.delete("/{income_id}", status_code=204)
async def delete_income(income_id: int, db: AsyncSession = Depends(get_db)):
    income = await db.get(Income, income_id)
    if not income:
        raise HTTPException(404, "Доход не найден")
    await db.delete(income)
    await db.commit()
