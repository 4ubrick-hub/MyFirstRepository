from app.db.db import SessionLocal
from app.db.models import Category, Book

db = SessionLocal()

try:
    print("\n" + "="*60)
    print("📚 БАЗА ДАННЫХ: КАТЕГОРИИ И КНИГИ")
    print("="*60 + "\n")
    
    # Получаем все категории
    categories = db.query(Category).all()
    
    for category in categories:
        print(f"📖 КАТЕГОРИЯ: {category.title}")
        print(f"   ID: {category.id}")
        
        # Получаем книги этой категории
        books = db.query(Book).filter(Book.category_id == category.id).all()
        
        if books:
            for book in books:
                print(f"   • {book.title}")
                print(f"     Описание: {book.description}")
                print(f"     Цена: {book.price} руб.")
                print()
        else:
            print("   (нет книг)\n")
    
    # Статистика
    total_categories = db.query(Category).count()
    total_books = db.query(Book).count()
    
    print("="*60)
    print(f"📊 СТАТИСТИКА: {total_categories} категорий, {total_books} книг")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"✗ Ошибка: {e}")
finally:
    db.close()
