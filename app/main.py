from fastapi import FastAPI

from app.db.db import engine
from app.db import models

from app.api.books import router as books_router
from app.api.categories import router as categories_router

# Создание таблиц (если их ещё нет)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Store API",
    description="REST API для управления книгами и категориями",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(categories_router)
app.include_router(books_router)


@app.get("/health", tags=["Info"])
def health():
    """Проверка работоспособности API"""
    return {
        "status": "OK",
        "message": "API работает корректно"
    }


@app.get("/", tags=["Info"])
def root():
    """Главная страница API"""
    return {
        "message": "Добро пожаловать в Book Store API!",
        "docs": "/docs",
        "health": "/health"
    }