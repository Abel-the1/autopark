from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Driver
from app.schemas.driver import DriverCreate, DriverUpdate, DriverOut

router = APIRouter()


@router.get("/", response_model=list[DriverOut])
async def list_drivers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Driver).order_by(Driver.id))
    return result.scalars().all()


@router.post("/", response_model=DriverOut, status_code=201)
async def create_driver(data: DriverCreate, db: AsyncSession = Depends(get_db)):
    driver = Driver(**data.model_dump())
    db.add(driver)
    await db.commit()
    await db.refresh(driver)
    return driver


@router.get("/{driver_id}", response_model=DriverOut)
async def get_driver(driver_id: int, db: AsyncSession = Depends(get_db)):
    driver = await db.get(Driver, driver_id)
    if not driver:
        raise HTTPException(404, "Водитель не найден")
    return driver


@router.patch("/{driver_id}", response_model=DriverOut)
async def update_driver(driver_id: int, data: DriverUpdate, db: AsyncSession = Depends(get_db)):
    driver = await db.get(Driver, driver_id)
    if not driver:
        raise HTTPException(404, "Водитель не найден")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(driver, field, value)
    await db.commit()
    await db.refresh(driver)
    return driver


@router.delete("/{driver_id}", status_code=204)
async def delete_driver(driver_id: int, db: AsyncSession = Depends(get_db)):
    driver = await db.get(Driver, driver_id)
    if not driver:
        raise HTTPException(404, "Водитель не найден")
    await db.delete(driver)
    await db.commit()
