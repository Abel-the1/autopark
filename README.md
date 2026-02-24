# 🚗 Autopark — система учёта автопарка

Система управления расходами и доходами арендного автопарка.

## Компоненты
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy
- **Bot**: Telegram (aiogram 3.x) — ввод данных
- **Frontend**: React — аналитический дашборд

## Быстрый старт

```bash
cp .env.example .env
# Заполни .env своими значениями
docker-compose up --build
```

## Доступ
- API: http://localhost:8000/docs
- Dashboard: http://localhost:3000
