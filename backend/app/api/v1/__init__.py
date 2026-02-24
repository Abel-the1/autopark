from fastapi import APIRouter
from app.api.v1 import cars, drivers, expenses, incomes, categories, analytics

router = APIRouter()

router.include_router(cars.router, prefix="/cars", tags=["Cars"])
router.include_router(drivers.router, prefix="/drivers", tags=["Drivers"])
router.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])
router.include_router(incomes.router, prefix="/incomes", tags=["Incomes"])
router.include_router(categories.router, prefix="/categories", tags=["Categories"])
router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
