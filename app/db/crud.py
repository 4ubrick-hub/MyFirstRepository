from sqlalchemy.orm import Session
from app.db.models import Book, Category

# ============ CATEGORY CRUD ============

def create_category(db: Session, title: str):
    """Создать новую категорию"""
    db_category = Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int):
    """Получить категорию по ID"""
    return db.query(Category).filter(Category.id == category_id).first()


def get_category_by_title(db: Session, title: str):
    """Получить категорию по названию"""
    return db.query(Category).filter(Category.title == title).first()


def get_all_categories(db: Session):
    """Получить все категории"""
    return db.query(Category).all()


def update_category(db: Session, category_id: int, title: str):
    """Обновить категорию"""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db_category.title = title
        db.commit()
        db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int):
    """Удалить категорию"""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category


# ============ BOOK CRUD ============

def create_book(db: Session, title: str, description: str, price: float, 
                category_id: int, url: str = None):
    """Создать новую книгу"""
    db_book = Book(
        title=title,
        description=description,
        price=price,
        category_id=category_id,
        url=url
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_book(db: Session, book_id: int):
    """Получить книгу по ID"""
    return db.query(Book).filter(Book.id == book_id).first()


def get_all_books(db: Session):
    """Получить все книги"""
    return db.query(Book).all()


def get_books_by_category(db: Session, category_id: int):
    """Получить все книги в категории"""
    return db.query(Book).filter(Book.category_id == category_id).all()


def update_book(db: Session, book_id: int, title: str = None, description: str = None,
                price: float = None, url: str = None, category_id: int = None):
    """Обновить книгу"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        if title is not None:
            db_book.title = title
        if description is not None:
            db_book.description = description
        if price is not None:
            db_book.price = price
        if url is not None:
            db_book.url = url
        if category_id is not None:
            db_book.category_id = category_id
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    """Удалить книгу"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
