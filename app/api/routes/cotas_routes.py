# Importação de módulos necessários
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.cota_model import Cota
from app.schemas.schemas import CotaCreate, CotaResponse, CotaProfitResponse
from app.crud import crud
from app.database.database import get_db
from typing import List

# Criando nova APIRouter
router = APIRouter()


# Adicionando endpoint para calcular o lucro de uma cota (cota de investimento)
@router.get("/cotas/{cota_id}/profit", response_model=CotaProfitResponse)
def get_cota_profit(cota_id: int, db: Session = Depends(get_db)):
    """
    Calcula o lucro e a rentabilidade (profitability) de uma cota específica.

    Args:
        cota_id (int): ID da cota.
        db (Session): Sessão do banco de dados.

    Returns:
        dict: Valores bruto, líquido e rentabilidade da cota.
    """
    cota = crud.get_cota(db, cota_id)
    if not cota:
        raise HTTPException(status_code=404, detail="Cota não encontrada.")

    # Calcula os valores bruto, líquido e rentabilidade
    gross_value, net_value, profitability = crud.calculate_cota_values(
        cota.amount, cota.interest_rate, cota.duration_months, cota.tax
    )

    return {
        "cota_id": cota_id,
        "gross_value": gross_value,
        "net_value": net_value,
        "profitability": profitability
    }


# Adicionando endpoint para criar uma cota (cota de investimento)
@router.post("/", response_model=CotaResponse, status_code=status.HTTP_201_CREATED)
def create_cota_endpoint(cota: CotaCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova cota de investimento.

    Args:
        cota (CotaCreate): Dados da cota a ser criada.
        db (Session): Sessão do banco de dados.

    Returns:
        CotaResponse: Dados da cota criada.
    """
    # Verificando se algum valor é negativo e levantando erro 422 com mensagem apropriada
    if cota.amount < 0:
        raise HTTPException(status_code=422, detail="O valor deve ser maior que 0.")
    if cota.interest_rate < 0:
        raise HTTPException(status_code=422, detail="A taxa de juros deve ser maior que 0.")
    if cota.duration_months < 0:
        raise HTTPException(status_code=422, detail="A duração em meses deve ser maior que 0.")

    # Criação da cota
    return crud.create_cota(db, cota)


# Adicionando endpoint para buscar uma cota (cota de investimento) específica
@router.get("/{cota_id}", response_model=CotaResponse)
def get_cota(cota_id: int, db: Session = Depends(get_db)):
    """
    Busca uma cota específica pelo ID.

    Args:
        cota_id (int): ID da cota.
        db (Session): Sessão do banco de dados.

    Returns:
        CotaResponse: Dados da cota encontrada.
    """
    db_cota = db.query(Cota).filter(Cota.id == cota_id).first()
    if db_cota is None:
        raise HTTPException(status_code=404, detail="Cota não encontrada.")
    return db_cota


# Adicionando endpoint para listar todas as cotas (cotas de investimento) com paginação
@router.get("/", response_model=List[CotaResponse])
def list_cotas_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Lista todas as cotas com suporte a paginação.

    Args:
        skip (int): Número de registros a pular.
        limit (int): Número máximo de registros a retornar.
        db (Session): Sessão do banco de dados.

    Returns:
        list: Lista de cotas.
    """
    cotas = crud.list_cotas(db, skip=skip, limit=limit)
    return [CotaResponse.from_orm(cota) for cota in cotas]


# Adicionando endpoint para atualizar uma cota (cota de investimento)
@router.put("/{cota_id}", response_model=CotaResponse)
def update_cota_endpoint(cota_id: int, cota: CotaCreate, db: Session = Depends(get_db)):
    """
    Atualiza os dados de uma cota específica.

    Args:
        cota_id (int): ID da cota a ser atualizada.
        cota (CotaCreate): Dados atualizados da cota.
        db (Session): Sessão do banco de dados.

    Returns:
        CotaResponse: Dados da cota atualizada.
    """
    return crud.update_cota(db, cota_id, cota)


# Adicionando endpoint para deletar uma cota (cota de investimento)
@router.delete("/{cota_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cota_endpoint(cota_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma cota específica pelo ID.

    Args:
        cota_id (int): ID da cota a ser deletada.
        db (Session): Sessão do banco de dados.

    Returns:
        None: Retorna código 204 em caso de sucesso.
    """
    db_cota = crud.delete_cota(db, cota_id)
    if not db_cota:
        raise HTTPException(status_code=404, detail="Cota não encontrada.")
    return  # Nenhum retorno é necessário, o código 204 já indica sucesso