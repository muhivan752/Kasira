from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.models.base import BaseModel

class Outlet(BaseModel):
    __tablename__ = "outlets"

    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brands.id"), nullable=True, index=True)

    brand = relationship("Brand", back_populates="outlets")
    orders = relationship("Order", back_populates="outlet")

