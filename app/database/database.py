# Importações necessárias
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pegando a URL do banco de dados da variável de ambiente (com fallback para SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///cotaInvestments.sqlite")

# Criando a conexão com o banco de dados
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Criando a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()


# Dependência do banco para injeção de dependência no FastAPI
def get_db():
    """
    Obtém uma sessão do banco de dados para ser usada como dependência no FastAPI.

    Yields:
        Session: Sessão do banco de dados.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Erro ao acessar o banco de dados 'Cota Investments': {e}")
        raise e  # Levanta novamente a exceção para o FastAPI capturar
    finally:
        db.close()


# Teste de conexão ao iniciar a API
def test_db_connection():
    """
    Testa a conexão com o banco de dados ao iniciar a aplicação.
    """
    try:
        with engine.connect() as conn:
            logger.info("Conexão com o banco de dados 'Cota Investments' bem-sucedida!")
    except Exception as e:
        logger.error(f"Erro na conexão com o banco de dados 'Cota Investments': {e}")
