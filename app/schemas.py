from pydantic import BaseModel
from typing import Optional, List


# ===== Схемы категорий =====
class CategoryBase(BaseModel):
    title: str

class CategoryCreate(CategoryBase): pass

class Category(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# ===== Схемы книг =====
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = None
    category_id: int

class BookCreate(BookBase): pass

class Book(BookBase):
    id: int
    category: Optional[Category] = None
    class Config: from_attributes = True

# ===== Схемы коллекций =====
class CategoryWithBooks(Category):
    books: List[Book] = []
    class Config: from_attributes = True
