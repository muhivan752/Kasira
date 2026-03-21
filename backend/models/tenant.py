from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel

class Tenant(BaseModel):
    __tablename__ = "tenants"

    name = Column(String, nullable=False)
    schema_name = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean(), default=True)

    brands = relationship("Brand", back_populates="tenant")
