from app.db.db import SessionLocal, engine
from app.db.models import Base, Category, Book

# Создаём все таблицы
Base.metadata.create_all(bind=engine)
print("✓ Таблицы созданы успешно!")

db = SessionLocal()

try:
    # Очищаем старые данные (опционально)
    db.query(Book).delete()
    db.query(Category).delete()
    db.commit()
    print("✓ Старые данные удалены")
    
    # ===== КАТЕГОРИЯ 1: Фантастика =====
    cat1 = Category(title="Фантастика")
    db.add(cat1)
    db.flush()  # Даёт id
    
    book1_1 = Book(title="Война и мир", description="Классический роман", price=500.0, category_id=cat1.id)
    book1_2 = Book(title="Дюна", description="Научная фантастика", price=450.0, category_id=cat1.id)
    book1_3 = Book(title="Звёздные войны", description="Космическая эпопея", price=600.0, category_id=cat1.id)
    
    db.add(book1_1)
    db.add(book1_2)
    db.add(book1_3)
    
    # ===== КАТЕГОРИЯ 2: Детектив =====
    cat2 = Category(title="Детектив")
    db.add(cat2)
    db.flush()
    
    book2_1 = Book(title="Шерлок Холмс", description="Классический детектив", price=400.0, category_id=cat2.id)
    book2_2 = Book(title="Граф Монте-Кристо", description="Приключенческий детектив", price=550.0, category_id=cat2.id)
    book2_3 = Book(title="Убийство на Ориент-Экспрессе", description="Детективный роман", price=480.0, category_id=cat2.id)
    book2_4 = Book(title="Код да Винчи", description="Современный детектив", price=520.0, category_id=cat2.id)
    
    db.add(book2_1)
    db.add(book2_2)
    db.add(book2_3)
    db.add(book2_4)
    
    # Сохраняем всё в БД
    db.commit()
    
    print("✓ Категория 1 (Фантастика) добавлена с 3 книгами")
    print("✓ Категория 2 (Детектив) добавлена с 4 книгами")
    print("✓ ВСЕ ДАННЫЕ ДОБАВЛЕНЫ УСПЕШНО!")
    
except Exception as e:
    db.rollback()
    print(f"✗ Ошибка: {e}")
finally:
    db.close()
