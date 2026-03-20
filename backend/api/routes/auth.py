from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.api import deps
from backend.core import security
from backend.core.config import settings
from backend.models.user import User
from backend.schemas.token import Token

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    stmt = select(User).where(User.email == form_data.username, User.deleted_at == None)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/login/pin", response_model=Token)
async def login_with_pin(
    pin: str = Body(..., embed=True),
    current_user: User = Depends(deps.get_current_user),
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    """
    Login with PIN for POS access (requires valid JWT token first)
    """
    if not current_user.hashed_pin:
        raise HTTPException(status_code=400, detail="PIN not set for this user")
        
    if not security.verify_pin(pin, current_user.hashed_pin):
        raise HTTPException(status_code=400, detail="Incorrect PIN")
        
    # Return a new token or just success message depending on requirements
    # For now, returning success
    return {
        "access_token": "pin_verified",
        "token_type": "bearer"
    }
