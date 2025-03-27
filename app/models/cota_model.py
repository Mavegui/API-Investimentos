# Importações de módulos necessários
from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.database.database import Base


# Classe de modelo de cotas de investimento
class Cota(Base):
    """
    Modelo da tabela 'cota' (cotas de investimento).

    Atributos:
        - id (int): Chave primária.
        - name (str): Nome da cota.
        - amount (float): Valor investido.
        - interest_rate (float): Rentabilidade (% ao mês).
        - duration_months (int): Prazo (meses).
        - tax (float): Imposto fixo (15% por padrão).
        - gross_value (float): Valor bruto do investimento.
        - net_value (float): Valor líquido do investimento.
        - profitability (float): Rentabilidade do investimento.
        - created_at (datetime): Data de criação (preenchida automaticamente).
    """
    __tablename__ = "cotas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    interest_rate = Column(Float, nullable=False)
    duration_months = Column(Integer, nullable=False)
    tax = Column(Float, default=0.15)
    gross_value = Column(Float, nullable=True)
    net_value = Column(Float, nullable=True)
    profitability = Column(Float, nullable=True)
    created_at = Column(DateTime, default=func.now())
