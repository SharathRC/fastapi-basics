from fastapi import APIRouter

from app.api.endpoints import recipe


api_router = APIRouter()
api_router.include_router(recipe.router, prefix="/recipes", tags=["recipes"])