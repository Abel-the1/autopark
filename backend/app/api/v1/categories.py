from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import ExpenseCategory
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter()


@router.get("/", response_model=list[CategoryOut])
async def list_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ExpenseCategory).order_by(ExpenseCategory.id))
    return result.scalars().all()


@router.post("/", response_model=CategoryOut, status_code=201)
async def create_category(data: CategoryCreate, db: AsyncSession = Depends(get_db)):
    cat = ExpenseCategory(**data.model_dump())
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


@router.delete("/{cat_id}", status_code=204)
async def delete_category(cat_id: int, db: AsyncSession = Depends(get_db)):
    cat = await db.get(ExpenseCategory, cat_id)
    if not cat:
        raise HTTPException(404, "Категория не найдена")
    await db.delete(cat)
    await db.commit()
