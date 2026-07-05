from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.db import engine, get_db
from app.db import models, crud
from app import schemas

# Создание таблиц (если их нет)
models.Base.metadata.create_all(bind=engine)

# Инициализация FastAPI приложения
app = FastAPI(
    title="Book Store API",
    description="REST API для управления книгами и категориями",
    version="1.0.0"
)

# ===== КАТЕГОРИИ =====

@app.post("/categories/", response_model=schemas.Category, tags=["Categories"], status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Создаёт новую категорию"""
    try:
        return crud.create_category(db, category.title)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Категория с названием '{category.title}' уже существует"
        )

@app.get("/categories/", response_model=list[schemas.Category], tags=["Categories"])
def get_all_categories(db: Session = Depends(get_db)):
    """Возвращает все категории"""
    return crud.get_all_categories(db)

@app.get("/categories/{category_id}", response_model=schemas.CategoryWithBooks, tags=["Categories"])
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Возвращает категорию по ID с её книгами"""
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return category

@app.get("/categories/by-title/{title}", response_model=schemas.Category, tags=["Categories"])
def get_category_by_title(title: str, db: Session = Depends(get_db)):
    """Возвращает категорию по названию"""
    category = crud.get_category_by_title(db, title)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return category

@app.put("/categories/{category_id}", response_model=schemas.Category, tags=["Categories"])
def update_category(category_id: int, category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Обновляет категорию по ID"""
    updated = crud.update_category(db, category_id, category.title)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return updated

@app.delete("/categories/{category_id}", tags=["Categories"])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удаляет категорию по ID"""
    success = crud.delete_category(db, category_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return {"message": "Категория удалена"}

# ===== КНИГИ =====

@app.post("/books/", response_model=schemas.Book, tags=["Books"], status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Создаёт новую книгу"""
    # Проверка существования категории
    category = crud.get_category(db, book.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    
    return crud.create_book(db, book.title, book.description, book.price, book.category_id, book.url)

@app.get("/books/", response_model=list[schemas.Book], tags=["Books"])
def get_all_books(db: Session = Depends(get_db)):
    """Возвращает все книги"""
    return crud.get_all_books(db)

@app.get("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Возвращает книгу по ID"""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return book

@app.get("/books/by-category/{category_id}", response_model=list[schemas.Book], tags=["Books"])
def get_books_by_category(category_id: int, db: Session = Depends(get_db)):
    """Возвращает все книги в категории"""
    category = crud.get_category(db, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    return crud.get_books_by_category(db, category_id)

@app.put("/books/{book_id}", response_model=schemas.Book, tags=["Books"])
def update_book(book_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Обновляет книгу по ID"""
    # Проверка существования категории
    category = crud.get_category(db, book.category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Категория не найдена")
    
    updated = crud.update_book(db, book_id, book.title, book.description, book.price, book.url, book.category_id)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return updated

@app.delete("/books/{book_id}", tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удаляет книгу по ID"""
    success = crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Книга не найдена")
    return {"message": "Книга удалена"}

# ===== СЛУЖЕБНЫЕ ЭНДПОИНТЫ =====

@app.get("/health", tags=["Info"])
def health_check():
    """Проверка статуса сервиса"""
    return {"status": "OK", "message": "API работает корректно"}

@app.get("/", tags=["Info"])
def root():
    """Информация об API"""
    return {
        "message": "Добро пожаловать в Book Store API!",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }
