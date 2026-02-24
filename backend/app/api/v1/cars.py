from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Car
from app.schemas.car import CarCreate, CarUpdate, CarOut

router = APIRouter()


@router.get("/", response_model=list[CarOut])
async def list_cars(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Car).order_by(Car.id))
    return result.scalars().all()


@router.post("/", response_model=CarOut, status_code=201)
async def create_car(data: CarCreate, db: AsyncSession = Depends(get_db)):
    car = Car(**data.model_dump())
    db.add(car)
    await db.commit()
    await db.refresh(car)
    return car


@router.get("/{car_id}", response_model=CarOut)
async def get_car(car_id: int, db: AsyncSession = Depends(get_db)):
    car = await db.get(Car, car_id)
    if not car:
        raise HTTPException(404, "Машина не найдена")
    return car


@router.patch("/{car_id}", response_model=CarOut)
async def update_car(car_id: int, data: CarUpdate, db: AsyncSession = Depends(get_db)):
    car = await db.get(Car, car_id)
    if not car:
        raise HTTPException(404, "Машина не найдена")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(car, field, value)
    await db.commit()
    await db.refresh(car)
    return car


@router.delete("/{car_id}", status_code=204)
async def delete_car(car_id: int, db: AsyncSession = Depends(get_db)):
    car = await db.get(Car, car_id)
    if not car:
        raise HTTPException(404, "Машина не найдена")
    await db.delete(car)
    await db.commit()
