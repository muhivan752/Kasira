from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Any, List, Dict
import uuid

from backend.api import deps
from backend.schemas.sync import SyncRequest, SyncResponse, SyncPayload
from backend.models.user import User
from backend.models.category import Category
from backend.models.product import Product
from backend.models.order import Order, OrderItem
from backend.models.payment import Payment
from backend.models.outlet import Outlet
from backend.services.sync import process_table_sync, process_stock_sync, get_table_changes, utc_now
from backend.services.crdt import HLC

router = APIRouter()

@router.post("/", response_model=SyncResponse)
def sync_data(
    request: SyncRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Pure CRDT Sync Engine Endpoint (Pull & Push)
    """
    # Get user's outlet and brand context
    outlet = db.query(Outlet).filter(Outlet.id == current_user.outlet_id).first()
    if not outlet:
        raise HTTPException(status_code=400, detail="User is not assigned to an outlet")
        
    brand_id = outlet.brand_id
    outlet_id = outlet.id
    
    # Initialize Server HLC
    server_hlc = HLC.generate(node_id="server")
    
    # 1. PUSH (Apply changes from client to server)
    if request.changes:
        if request.changes.categories:
            process_table_sync(db, Category, request.changes.categories, {"brand_id": brand_id}, server_hlc)
        if request.changes.products:
            process_table_sync(db, Product, request.changes.products, {"brand_id": brand_id}, server_hlc)
        if request.changes.orders:
            process_table_sync(db, Order, request.changes.orders, {"outlet_id": outlet_id}, server_hlc)
        if request.changes.order_items:
            process_table_sync(db, OrderItem, request.changes.order_items, {}, server_hlc)
        if request.changes.payments:
            process_table_sync(db, Payment, request.changes.payments, {"outlet_id": outlet_id}, server_hlc)
        if request.changes.outlet_stock:
            process_stock_sync(db, request.changes.outlet_stock, outlet_id, server_hlc)
            
    # 2. PULL (Get changes from server to client since last_sync_hlc)
    client_last_sync_hlc = None
    if request.last_sync_hlc:
        try:
            client_last_sync_hlc = HLC.from_string(request.last_sync_hlc)
        except ValueError:
            pass # Invalid HLC string, pull everything
            
    pull_changes = SyncPayload(
        categories=get_table_changes(db, Category, {"brand_id": brand_id}, client_last_sync_hlc),
        products=get_table_changes(db, Product, {"brand_id": brand_id}, client_last_sync_hlc),
        orders=get_table_changes(db, Order, {"outlet_id": outlet_id}, client_last_sync_hlc),
        order_items=[],
        payments=get_table_changes(db, Payment, {"outlet_id": outlet_id}, client_last_sync_hlc),
        outlet_stock=[]
    )
    
    # Custom pull for order_items
    order_items_query = db.query(OrderItem).join(Order).filter(
        Order.outlet_id == outlet_id
    )
    if client_last_sync_hlc and client_last_sync_hlc.timestamp > 0:
        last_sync_dt = datetime.fromtimestamp(client_last_sync_hlc.timestamp / 1000.0, tz=timezone.utc)
        order_items_query = order_items_query.filter(OrderItem.updated_at >= last_sync_dt)
        
    order_items_records = order_items_query.all()
    oi_result = []
    for r in order_items_records:
        record_dict = {}
        for c in r.__table__.columns:
            val = getattr(r, c.name)
            if isinstance(val, datetime):
                record_dict[c.name] = val.isoformat()
            elif isinstance(val, uuid.UUID):
                record_dict[c.name] = str(val)
            else:
                record_dict[c.name] = val
                
        r_updated_at = getattr(r, "updated_at")
        if r_updated_at.tzinfo is None:
            r_updated_at = r_updated_at.replace(tzinfo=timezone.utc)
        r_timestamp = int(r_updated_at.timestamp() * 1000)
        r_counter = getattr(r, "row_version", 0)
        r_hlc = HLC(timestamp=r_timestamp, counter=r_counter, node_id="server")
        record_dict["hlc"] = r_hlc.to_string()
        oi_result.append(record_dict)
        
    pull_changes.order_items = oi_result
    
    # Custom pull for outlet_stock
    from backend.models.product import OutletStock
    stock_query = db.query(OutletStock).filter(OutletStock.outlet_id == outlet_id)
    if client_last_sync_hlc and client_last_sync_hlc.timestamp > 0:
        last_sync_dt = datetime.fromtimestamp(client_last_sync_hlc.timestamp / 1000.0, tz=timezone.utc)
        stock_query = stock_query.filter(OutletStock.updated_at >= last_sync_dt)
        
    stock_records = stock_query.all()
    stock_result = []
    for r in stock_records:
        record_dict = {}
        for c in r.__table__.columns:
            val = getattr(r, c.name)
            if isinstance(val, datetime):
                record_dict[c.name] = val.isoformat()
            elif isinstance(val, uuid.UUID):
                record_dict[c.name] = str(val)
            else:
                record_dict[c.name] = val
                
        r_updated_at = getattr(r, "updated_at")
        if r_updated_at.tzinfo is None:
            r_updated_at = r_updated_at.replace(tzinfo=timezone.utc)
        r_timestamp = int(r_updated_at.timestamp() * 1000)
        r_counter = getattr(r, "row_version", 0)
        r_hlc = HLC(timestamp=r_timestamp, counter=r_counter, node_id="server")
        record_dict["hlc"] = r_hlc.to_string()
        stock_result.append(record_dict)
        
    pull_changes.outlet_stock = stock_result
    
    return SyncResponse(
        last_sync_hlc=server_hlc.to_string(),
        changes=pull_changes
    )
