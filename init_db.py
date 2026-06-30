from app.db.db import engine, Base
from app.db.models import Book, Category

# Создаём все таблицы
Base.metadata.create_all(bind=engine)
print("✓ Таблицы созданы успешно!")
