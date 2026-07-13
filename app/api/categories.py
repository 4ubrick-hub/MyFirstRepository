from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.db import get_db
from app.db import crud
from app import schemas

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """Создать новую категорию"""

    try:
        return crud.create_category(db, category.title)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Категория '{category.title}' уже существует"
        )


@router.get("/", response_model=list[schemas.Category])
def get_categories(db: Session = Depends(get_db)):
    """Получить список категорий"""

    return crud.get_all_categories(db)


@router.get("/{category_id}", response_model=schemas.CategoryWithBooks)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Получить категорию по ID"""

    category = crud.get_category(db, category_id)

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    return category


@router.put("/{category_id}", response_model=schemas.Category)
def update_category(
    category_id: int,
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """Изменить категорию"""

    updated = crud.update_category(
        db,
        category_id,
        category.title
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    return updated


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию"""

    success = crud.delete_category(db, category_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )

    return {
        "message": "Категория удалена"
    }