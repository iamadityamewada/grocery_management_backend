from sqlalchemy.orm import Session
from typing import List, Optional

from app.models import models
from app.schemas import schemas

def get_grocery_item(db: Session, item_id: int) -> Optional[models.GroceryItem]:
    return db.query(models.GroceryItem).filter(models.GroceryItem.id == item_id).first()

def get_grocery_items_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[models.GroceryItem]:
    return db.query(models.GroceryItem).filter(models.GroceryItem.owner_id == owner_id).offset(skip).limit(limit).all()

def create_grocery_item(db: Session, item: schemas.GroceryItemCreate, owner_id: int) -> models.GroceryItem:
    db_item = models.GroceryItem(**item.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_grocery_item(db: Session, db_item: models.GroceryItem, item_update: schemas.GroceryItemUpdate) -> models.GroceryItem:
    update_data = item_update.model_dump(exclude_unset=True) # Get only provided fields
    for key, value in update_data.items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_grocery_item(db: Session, db_item: models.GroceryItem) -> None:
    db.delete(db_item)
    db.commit()
