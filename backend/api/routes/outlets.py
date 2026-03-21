import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.api import deps
from backend.models.outlet import Outlet
from backend.schemas.outlet import Outlet as OutletSchema, OutletCreate, OutletUpdate
from backend.schemas.response import StandardResponse, ResponseMeta
from backend.services.audit import log_audit
import json

router = APIRouter()

@router.get("/", response_model=StandardResponse[List[OutletSchema]])
async def read_outlets(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve outlets.
    """
    stmt = select(Outlet).where(Outlet.deleted_at == None).offset(skip).limit(limit)
    if not current_user.is_superuser:
        stmt = stmt.where(Outlet.tenant_id == current_user.tenant_id)
        
    result = await db.execute(stmt)
    outlets = result.scalars().all()
    
    meta = ResponseMeta(page=(skip // limit) + 1, per_page=limit, total=len(outlets))
    return StandardResponse(data=outlets, meta=meta)

@router.post("/", response_model=StandardResponse[OutletSchema])
async def create_outlet(
    *,
    db: AsyncSession = Depends(deps.get_db),
    outlet_in: OutletCreate,
    current_user: Any = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new outlet.
    """
    db_outlet = Outlet(**outlet_in.model_dump())
    db.add(db_outlet)
    await db.flush()
    
    after_state = json.loads(outlet_in.model_dump_json())
    await log_audit(
        db=db,
        action="CREATE",
        entity="outlets",
        entity_id=db_outlet.id,
        after_state=after_state,
        user_id=current_user.id,
        tenant_id=db_outlet.tenant_id
    )
    
    await db.commit()
    await db.refresh(db_outlet)
    return StandardResponse(data=db_outlet, message="Outlet created successfully")

@router.get("/{outlet_id}", response_model=StandardResponse[OutletSchema])
async def read_outlet(
    outlet_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: Any = Depends(deps.get_current_user),
) -> Any:
    """
    Get outlet by ID.
    """
    stmt = select(Outlet).where(Outlet.id == outlet_id, Outlet.deleted_at == None)
    if not current_user.is_superuser:
        stmt = stmt.where(Outlet.tenant_id == current_user.tenant_id)
        
    result = await db.execute(stmt)
    outlet = result.scalar_one_or_none()
    if not outlet:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return StandardResponse(data=outlet)
