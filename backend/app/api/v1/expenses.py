from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseOut
import datetime

router = APIRouter()


@router.get("/", response_model=list[ExpenseOut])
async def list_expenses(
    car_id: int | None = Query(None),
    driver_id: int | None = Query(None),
    date_from: datetime.date | None = Query(None),
    date_to: datetime.date | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    q = select(Expense).options(
        selectinload(Expense.car),
        selectinload(Expense.driver),
        selectinload(Expense.category),
    )
    if car_id:
        q = q.where(Expense.car_id == car_id)
    if driver_id:
        q = q.where(Expense.driver_id == driver_id)
    if date_from:
        q = q.where(Expense.date >= date_from)
    if date_to:
        q = q.where(Expense.date <= date_to)
    q = q.order_by(Expense.date.desc())
    result = await db.execute(q)
    return result.scalars().all()


@router.post("/", response_model=ExpenseOut, status_code=201)
async def create_expense(data: ExpenseCreate, db: AsyncSession = Depends(get_db)):
    expense = Expense(**data.model_dump())
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense


@router.get("/{expense_id}", response_model=ExpenseOut)
async def get_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    expense = await db.get(Expense, expense_id)
    if not expense:
        raise HTTPException(404, "Расход не найден")
    return expense


@router.patch("/{expense_id}", response_model=ExpenseOut)
async def update_expense(expense_id: int, data: ExpenseUpdate, db: AsyncSession = Depends(get_db)):
    expense = await db.get(Expense, expense_id)
    if not expense:
        raise HTTPException(404, "Расход не найден")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(expense, field, value)
    await db.commit()
    await db.refresh(expense)
    return expense


@router.delete("/{expense_id}", status_code=204)
async def delete_expense(expense_id: int, db: AsyncSession = Depends(get_db)):
    expense = await db.get(Expense, expense_id)
    if not expense:
        raise HTTPException(404, "Расход не найден")
    await db.delete(expense)
    await db.commit()
