# Importa APIRouter e rotas da API
from fastapi import APIRouter
from api.routes import router as api_router

# Cria nova APIRouter
router = APIRouter()
# Inclui rotas da API
router.include_router(api_router, prefix="/api")
