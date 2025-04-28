from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, grocery_items

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(grocery_items.router, prefix="/groceries", tags=["Grocery Items"])
