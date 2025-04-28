from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas import schemas
from app.models import models
from app.crud import grocery_items as crud_items
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.GroceryItem, status_code=status.HTTP_201_CREATED)
async def create_grocery_item(
    item_in: schemas.GroceryItemCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Create a new grocery item for the current user.
    """
    return crud_items.create_grocery_item(db=db, item=item_in, owner_id=current_user.id)


@router.get("/", response_model=List[schemas.GroceryItem])
async def read_grocery_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve grocery items for the current user.
    """
    items = crud_items.get_grocery_items_by_owner(db, owner_id=current_user.id, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=schemas.GroceryItem)
async def read_grocery_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Retrieve a specific grocery item by ID.
    """
    db_item = crud_items.get_grocery_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grocery item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this item")
    return db_item


@router.put("/{item_id}", response_model=schemas.GroceryItem)
async def update_grocery_item(
    item_id: int,
    item_in: schemas.GroceryItemUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update a specific grocery item by ID.
    """
    db_item = crud_items.get_grocery_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grocery item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this item")

    updated_item = crud_items.update_grocery_item(db=db, db_item=db_item, item_update=item_in)
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_grocery_item(
    item_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Delete a specific grocery item by ID.
    """
    db_item = crud_items.get_grocery_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grocery item not found")
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this item")

    crud_items.delete_grocery_item(db=db, db_item=db_item)
    # No content to return, status code 204 handled by decorator
    return None
