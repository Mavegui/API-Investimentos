from fastapi import APIRouter
from .cotas_routes import router as cotas_router


router = APIRouter()
router.include_router(cotas_router, prefix="/cotas", tags=["Cotas"])
