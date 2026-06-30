from sqlalchemy import text
from app.db.db import SessionLocal

try:
    db = SessionLocal()
    db.execute(text("SELECT 1"))
    print("✓ Подключение к БД работает!")
    db.close()
except Exception as e:
    print(f"✗ Ошибка подключения: {e}")
