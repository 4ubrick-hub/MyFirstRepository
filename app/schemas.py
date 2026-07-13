from typing import List, Optional

from pydantic import BaseModel, Field


# ---------- Categories ----------

class CategoryBase(BaseModel):
    title: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# ---------- Books ----------

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    url: Optional[str] = None
    category_id: int


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    category: Optional[Category] = None

    class Config:
        from_attributes = True


# ---------- Collections ----------

class CategoryWithBooks(Category):
    books: List[Book] = Field(default_factory=list)

    class Config:
        from_attributes = True