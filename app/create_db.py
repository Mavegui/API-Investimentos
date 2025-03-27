# Importando banco de dados e criando as tabelas
from app.database.database import engine, Base
# Importando o modelo para criar as tabelas no banco de dados
from app.models.cota_model import Cota

# Criando as tabelas no banco de dados
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Banco de dados atualizado com sucesso!")
