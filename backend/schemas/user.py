from typing import Optional
from pydantic import BaseModel, EmailStr, UUID4
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    tenant_id: Optional[UUID4] = None
    role_id: Optional[UUID4] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    full_name: str
    tenant_id: UUID4

class UserCreateWithPIN(UserCreate):
    pin: Optional[str] = None

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None
    pin: Optional[str] = None

class UserInDBBase(UserBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    row_version: int

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
    hashed_pin: Optional[str] = None
