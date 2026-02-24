"""Заполнение начальных категорий расходов"""
import asyncio
from app.database import AsyncSessionLocal
from app.models import ExpenseCategory
from sqlalchemy import select

DEFAULT_CATEGORIES = [
    "Топливо",
    "Техническое обслуживание",
    "Штраф",
    "Страховка",
    "Мойка",
    "Шины",
    "Запчасти",
    "Прочее",
]


async def seed():
    async with AsyncSessionLocal() as db:
        existing = (await db.execute(select(ExpenseCategory))).scalars().all()
        existing_names = {c.name for c in existing}
        for name in DEFAULT_CATEGORIES:
            if name not in existing_names:
                db.add(ExpenseCategory(name=name))
        await db.commit()
        print(f"Категории добавлены: {len(DEFAULT_CATEGORIES) - len(existing_names)} новых")


if __name__ == "__main__":
    asyncio.run(seed())
