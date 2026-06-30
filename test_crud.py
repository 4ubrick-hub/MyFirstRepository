from app.db.db import SessionLocal
from app.db.crud import create_category, get_all_categories, create_book, get_all_books

db = SessionLocal()

try:
    # Создаём категорию
    cat = create_category(db, "Фантастика")
    print(f"✓ Категория создана: {cat}")
    
    # Получаем все категории
    categories = get_all_categories(db)
    print(f"✓ Категории: {categories}")
    
    # Создаём книгу
    book = create_book(db, "Война и мир", "Классический роман", 500.0, cat.id)
    print(f"✓ Книга создана: {book}")
    
    # Получаем все книги
    books = get_all_books(db)
    print(f"✓ Книги: {books}")
    
    print("\n✓ ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    
except Exception as e:
    print(f"✗ Ошибка: {e}")
finally:
    db.close()
