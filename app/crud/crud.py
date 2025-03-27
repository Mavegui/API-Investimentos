# Importando módulos necessários
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.cota_model import Cota
from app.schemas.schemas import CotaCreate, CotaResponse
from fastapi import HTTPException
from decimal import Decimal


# Função para calcular rentabilidade da cota de investimento, antes de salvar
def calculate_cota_values(amount: float, interest_rate: float, duration: int, tax: float):
    """
    Calcula os valores bruto, líquido e a rentabilidade de uma cota.

    Args:
        amount (float): Valor inicial da cota.
        interest_rate (float): Taxa de juros anual.
        duration (int): Duração em meses.
        tax (float): Taxa de imposto.

    Returns:
        tuple: Valores bruto, líquido e rentabilidade da cota.
    """
    # Verifica se os valores são válidos
    if amount <= 0 or interest_rate <= 0 or duration <= 0 or tax < 0:
        raise ValueError("Todos os valores devem ser positivos e a taxa não pode ser negativa.")

    # Cálculo de rendimento com juros simples
    profitability = amount * (interest_rate / 100) * duration
    gross_value = amount + profitability
    tax_value = profitability * tax
    net_value = gross_value - tax_value

    return gross_value, net_value, profitability


# Cria uma cota (cota de investimento)
def create_cota(db: Session, cota: CotaCreate):
    """
    Cria uma nova cota no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        cota (CotaCreate): Dados da cota a ser criada.

    Returns:
        Cota: Objeto da cota criada.
    """
    try:
        gross_value, net_value, profitability = calculate_cota_values(
            cota.amount, cota.interest_rate, cota.duration_months, 0.15
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    db_cota = Cota(
        **cota.model_dump(),
        gross_value=gross_value,
        net_value=net_value,
        profitability=profitability  # Salva a rentabilidade
    )
    db.add(db_cota)
    db.commit()
    db.refresh(db_cota)
    return db_cota


# Busca uma cota (cota de investimento) pelo ID
def get_cota(db: Session, cota_id: int):
    """
    Busca uma cota pelo ID no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        cota_id (int): ID da cota.

    Returns:
        Cota: Objeto da cota encontrada ou None se não existir.
    """
    return db.query(Cota).filter(Cota.id == cota_id).first()


# Lista todas as cotas (cotas de investimentos) com paginação
def list_cotas(db: Session, skip: int = 0, limit: int = 100):
    """
    Lista todas as cotas com suporte a paginação.

    Args:
        db (Session): Sessão do banco de dados.
        skip (int): Número de registros a pular.
        limit (int): Número máximo de registros a retornar.

    Returns:
        list: Lista de cotas no formato Pydantic.
    """
    cotas = db.query(Cota).offset(skip).limit(limit).all()
    return [CotaResponse.from_orm(cota) for cota in cotas]


# Atualiza uma cota (cota de investimento) pelo ID
def update_cota(db: Session, cota_id: int, cota: CotaCreate):
    """
    Atualiza os dados de uma cota específica.

    Args:
        db (Session): Sessão do banco de dados.
        cota_id (int): ID da cota a ser atualizada.
        cota (CotaCreate): Dados atualizados da cota.

    Returns:
        Cota: Objeto da cota atualizada.
    """
    # Busca a cota no banco de dados
    db_cota = db.query(Cota).filter(Cota.id == cota_id).first()

    if db_cota is None:
        raise HTTPException(status_code=404, detail="Cota não encontrada.")

    # Atualiza os dados da cota (cota de investimento)
    db_cota.name = cota.name
    db_cota.amount = cota.amount
    db_cota.interest_rate = cota.interest_rate
    db_cota.duration_months = cota.duration_months

    # Calcula os valores de gross_value (valor bruto), net_value (valor líquido) e profitability (rentabilidade)
    gross_value, net_value, profitability = calculate_cota_values(
        cota.amount, cota.interest_rate, cota.duration_months, db_cota.tax
    )

    # Atualiza os valores calculados no banco
    db_cota.gross_value = gross_value
    db_cota.net_value = net_value
    db_cota.profitability = profitability  # Atualiza a rentabilidade

    # Commit e refresh do banco de dados
    db.commit()
    db.refresh(db_cota)

    return db_cota


# Deleta uma cota (cota de investimento)
def delete_cota(db: Session, cota_id: int):
    """
    Deleta uma cota específica pelo ID.

    Args:
        db (Session): Sessão do banco de dados.
        cota_id (int): ID da cota a ser deletada.

    Returns:
        Cota: Objeto da cota deletada.
    """
    db_cota = db.query(Cota).filter(Cota.id == cota_id).first()
    if db_cota is None:
        raise HTTPException(status_code=404, detail="Cota não encontrada.")

    db.delete(db_cota)
    db.commit()

    return db_cota

