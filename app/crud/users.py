from sqlalchemy.orm import Session
from typing import Optional

from app.models import models
from app.schemas import schemas
from app.core.security import get_password_hash

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: models.User, user_update: schemas.UserUpdate) -> models.User:
    # Currently, no fields are directly updatable via UserUpdate schema
    # Password update is handled separately. Email changes might need verification.
    # If you add fields like 'is_active' to UserUpdate, update them here.
    # e.g., if user_update.is_active is not None: user.is_active = user_update.is_active
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user: models.User, new_password: str) -> models.User:
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user: models.User) -> None:
    # Note: Related grocery items will be deleted due to cascade="all, delete-orphan"
    db.delete(user)
    db.commit()
