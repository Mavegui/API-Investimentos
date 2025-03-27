# Importação de módulos necessários
from pydantic import BaseModel, Field
from datetime import datetime


# Classe para validação de dados de entrada
class CotaCreate(BaseModel):
    """
    Esquema para criação de uma nova cota (cota de investimento).

    Atributos:
        - name (str): Nome da cota (entre 3 e 50 caracteres).
        - amount (float): Valor investido (maior que 0).
        - interest_rate (float): Taxa de juros (maior que 0).
        - duration_months (int): Duração em meses (maior que 0).
    """
    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="O nome deve ter entre 3 e 50 caracteres."
    )
    amount: float = Field(
        ...,
        gt=0,
        description="O valor investido deve ser maior que 0."
    )
    interest_rate: float = Field(
        ...,
        gt=0,
        description="A taxa de juros deve ser maior que 0."
    )
    duration_months: int = Field(
        ...,
        gt=0,
        description="A duração deve ser maior que 0."
    )

    model_config = {"from_attributes": True}


# Classe para validação de dados de saída
class CotaResponse(CotaCreate):
    """
    Esquema para resposta de uma cota (cota de investimento).

    Atributos:
        - id (int): Identificador único da cota.
        - amount: Valor investido sendo serializado como float.
        - interest_rate: Taxa de juros sendo serializado como float.
        - created_at (datetime): Data de criação da cota.
        - tax (float): Imposto fixo (15%).
    """
    id: int
    created_at: datetime
    tax: float = 0.15

    model_config = {"from_attributes": True}


# Classe para resposta do endpoint /cotas/{cota_id}/profit
class CotaProfitResponse(BaseModel):
    """
    Esquema para resposta do cálculo de lucro e rentabilidade de uma cota.

    Atributos:
        - cota_id (int): Identificador único da cota.
        - gross_value (float): Valor bruto da cota.
        - net_value (float): Valor líquido da cota.
        - profitability (float): Rentabilidade da cota.
    """
    cota_id: int
    gross_value: float
    net_value: float
    profitability: float