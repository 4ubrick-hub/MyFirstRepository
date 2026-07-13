# Book Store API

REST API для управления книгами и категориями.

## Используемые технологии

- Python 3
- FastAPI
- SQLAlchemy
- PostgreSQL
- Uvicorn

---

## Установка

### Клонирование проекта

```bash
git clone https://github.com/4ubrick-hub/MyFirstRepository.git

cd MyFirstRepository
```

### Создание виртуального окружения

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux

```bash
source venv/bin/activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## Настройка PostgreSQL

Создать базу данных PostgreSQL.

Открыть файл app/db/db.py и указать:

- host
- port
- database
- username
- password

```
app/db/db.py
```

---

## Создание таблиц

```bash
python app/init_db.py
```

---

## Запуск сервера

```bash
uvicorn app.main:app --reload
```

После успешного запуска открыть

http://127.0.0.1:8000/docs

для просмотра Swagger UI.

---

## Swagger

После запуска открыть

```
http://127.0.0.1:8000/docs
```

---

## Проверка работы

```
GET /health
```

Ответ

```json
{
  "status": "OK",
  "message": "API работает корректно"
}
```