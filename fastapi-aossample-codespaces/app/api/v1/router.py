from fastapi import APIRouter
from .endpoints import tasks, auth

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(tasks.router)
api_router.include_router(auth.router)
