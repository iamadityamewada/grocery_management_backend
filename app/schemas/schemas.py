from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from app.models.models import GroceryStatus # Import Enum from models

# Grocery Item Schemas
class GroceryItemBase(BaseModel):
    name: str = Field(..., min_length=1, examples=["Apples"])
    quantity: int = Field(..., gt=0, examples=[5])
    status: GroceryStatus = Field(default=GroceryStatus.pending, examples=["pending"])

class GroceryItemCreate(GroceryItemBase):
    pass

class GroceryItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, examples=["Organic Milk"])
    quantity: Optional[int] = Field(None, gt=0, examples=[2])
    status: Optional[GroceryStatus] = Field(None, examples=["purchased"])

class GroceryItem(GroceryItemBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True # Pydantic V2 compatibility (orm_mode)


# User Schemas
class UserBase(BaseModel):
    email: EmailStr = Field(..., examples=["test@user.com"])

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, examples=["12345678"])

class UserUpdate(BaseModel):
    # Currently only supporting password update via separate endpoint
    # email: Optional[EmailStr] = None # Email changes might require verification
    # is_active: Optional[bool] = None # Admin functionality?
    pass

class UserPasswordUpdate(BaseModel):
    current_password: str = Field(..., examples=["OldSecurePassword"])
    new_password: str = Field(..., min_length=8, examples=["NewSecurePassword456"])

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    # No longer include grocery_items here by default to avoid large responses
    # grocery_items: List[GroceryItem] = []

    class Config:
         from_attributes = True # Pydantic V2 compatibility (orm_mode)


# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

# Generic Message Schema
class Message(BaseModel):
    message: str
