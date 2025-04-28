from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models import models
from app.schemas import schemas
from app.crud import users as crud_users
from app.api import deps
from app.core import security # For password verification

router = APIRouter()


@router.get("/me", response_model=schemas.User)
async def read_users_me(
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    user_in: schemas.UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update own user. Currently limited, main use is via password update.
    """
    # You might add fields like 'name' here later
    # For now, this endpoint doesn't change much directly
    updated_user = crud_users.update_user(db=db, user=current_user, user_update=user_in)
    return updated_user


@router.put("/me/password", response_model=schemas.Message)
async def update_password_me(
    password_update: schemas.UserPasswordUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Update own password.
    """
    if not security.verify_password(password_update.current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect current password")
    if password_update.current_password == password_update.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password cannot be the same as the old password")

    crud_users.update_user_password(db=db, user=current_user, new_password=password_update.new_password)
    return {"message": "Password updated successfully"}


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    """
    Delete own user account.
    """
    crud_users.delete_user(db=db, user=current_user)
    # No content to return, status code 204 handled by decorator
    return None

# Example: Admin endpoint (requires additional permission checks - not implemented here)
# @router.get("/", response_model=List[schemas.User])
# async def read_users(
#     skip: int = 0,
#     limit: int = 100,
#     db: Session = Depends(deps.get_db),
#     # current_user: models.User = Depends(deps.get_current_admin_user), # Example permission
# ):
#     """
#     Retrieve users (requires admin privileges).
#     """
#     users = crud_users.get_users(db, skip=skip, limit=limit)
#     return users

# Example: Get specific user by ID (requires permissions)
# @router.get("/{user_id}", response_model=schemas.User)
# async def read_user_by_id(
#     user_id: int,
#     db: Session = Depends(deps.get_db),
#     # current_user: models.User = Depends(deps.get_current_admin_user), # Example permission
# ):
#     """
#     Get a specific user by ID (requires admin privileges).
#     """
#     db_user = crud_users.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     return db_user
