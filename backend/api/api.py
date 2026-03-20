from fastapi import APIRouter
from backend.api.routes import auth, users, tenants, outlets

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(outlets.router, prefix="/outlets", tags=["outlets"])
