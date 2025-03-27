# Importando FastAPI e as rotas de cotas
from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.api.routes.cotas_routes import router as cotas_router


# Cria aplicação FastAPI com título, descrição e versão
app = FastAPI(
    title="API de Cotas",
    description="API para gerenciamento de cotas de investimentos",
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Manipulador de exceções para erros de validação de dados.

    Args:
        request (Request): Requisição que gerou o erro.
        exc (RequestValidationError): Exceção de validação.

    Returns:
        JSONResponse: Resposta com detalhes do erro.
    """
    return JSONResponse(
        status_code=422,
        content={
            "detalhe": "Houve um erro de validação nos dados fornecidos.",
            "erros": exc.errors(),
            "corpo": exc.body.decode("utf-8") if hasattr(exc.body, "decode") else exc.body,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Manipulador de exceções para erros HTTP.

    Args:
        request (Request): Requisição que gerou o erro.
        exc (HTTPException): Exceção HTTP.

    Returns:
        JSONResponse: Resposta com detalhes do erro.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detalhe": exc.detail},
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Manipulador de exceções para erros de banco de dados.

    Args:
        request (Request): Requisição que gerou o erro.
        exc (SQLAlchemyError): Exceção do SQLAlchemy.

    Returns:
        JSONResponse: Resposta com detalhes do erro.
    """
    return JSONResponse(
        status_code=500,
        content={
            "detalhe": "Erro interno no banco de dados. Por favor, tente novamente mais tarde."
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """
    Manipulador de exceções genéricas.

    Args:
        request (Request): Requisição que gerou o erro.
        exc (Exception): Exceção genérica.

    Returns:
        JSONResponse: Resposta com detalhes do erro.
    """
    return JSONResponse(
        status_code=500,
        content={
            "detalhe": "Ocorreu um erro inesperado. Por favor, tente novamente mais tarde."
        },
    )


# Adiciona as rotas de cotas à aplicação
app.include_router(cotas_router, prefix="/cotas", tags=["Cotas"])
