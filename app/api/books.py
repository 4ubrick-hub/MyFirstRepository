from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app import schemas

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Создаёт новую книгу"""

    category = crud.get_category(db, book.category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    return crud.create_book(
        db,
        book.title,
        book.description,
        book.price,
        book.category_id,
        book.url
    )


@router.get("/", response_model=list[schemas.Book])
def get_all_books(
    category_id: int | None = None,
    db: Session = Depends(get_db)
):
    """
    Возвращает все книги.

    Если указан category_id,
    возвращает книги только этой категории.
    """

    if category_id is not None:

        category = crud.get_category(db, category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Категория не найдена"
            )

        return crud.get_books_by_category(db, category_id)

    return crud.get_all_books(db)


@router.get("/{book_id}", response_model=schemas.Book)
def get_book(book_id: int, db: Session = Depends(get_db)):

    book = crud.get_book(db, book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    return book


@router.put("/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int,
    book: schemas.BookCreate,
    db: Session = Depends(get_db)
):

    category = crud.get_category(db, book.category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    updated = crud.update_book(
        db,
        book_id,
        book.title,
        book.description,
        book.price,
        book.url,
        book.category_id
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    return updated


@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):

    success = crud.delete_book(db, book_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Книга не найдена"
        )

    return {"message": "Книга удалена"}