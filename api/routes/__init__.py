from fastapi import APIRouter
from .employee import router as employee_router
from .org_chart import router as org_chart_router

api_router = APIRouter()
api_router.include_router(org_chart_router)
api_router.include_router(employee_router)
