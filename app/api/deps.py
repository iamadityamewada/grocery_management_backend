from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from pydantic import ValidationError

from app.core.database import get_db
from app.core import security
from app.core.config import settings
from app.models import models
from app.schemas import schemas
from app.crud import users as crud_users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        print(payload)
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
        email = email[9:(len(email)-2)]
        print(email)
        token_data = schemas.TokenData(email=email)
        print(token_data)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = crud_users.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    if not user.is_active:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user

async def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    # This dependency is useful if you have roles or further checks later
    # For now, it just ensures the user is active via get_current_user
    return current_user
