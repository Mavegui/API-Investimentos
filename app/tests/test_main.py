import pytest
from fastapi.testclient import TestClient
import sys
import os

# Adicionando o caminho do app para os imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../app')))
from app.main import app

client = TestClient(app)


def test_create_cota():
    """
    Testa a criação de uma nova cota.
    """
    cota_data = {
        "name": "Cota A",
        "amount": 2000.0,
        "interest_rate": 1.5,
        "duration_months": 12
    }
    response = client.post("/cotas/", json=cota_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == cota_data["name"]
    assert data["amount"] == cota_data["amount"]


def test_get_cota():
    """
    Testa a busca de uma cota específica pelo ID.
    """
    cota_data = {
        "name": "Cota B",
        "amount": 2000,
        "interest_rate": 2,
        "duration_months": 24
    }
    response = client.post("/cotas/", json=cota_data)
    assert response.status_code == 201
    created_cota = response.json()

    response = client.get(f"/cotas/{created_cota['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_cota["id"]
    assert data["name"] == cota_data["name"]
    assert data["amount"] == cota_data["amount"]


def test_update_cota():
    """
    Testa a atualização de uma cota existente.
    """
    cota_data = {
        "name": "Cota C",
        "amount": 3000,
        "interest_rate": 3,
        "duration_months": 36
    }
    response = client.post("/cotas/", json=cota_data)
    assert response.status_code == 201
    created_cota = response.json()

    update_data = {
        "name": "Cota C Atualizada",
        "amount": 3500,
        "interest_rate": 3.5,
        "duration_months": 40
    }
    response = client.put(f"/cotas/{created_cota['id']}", json=update_data)
    assert response.status_code == 200
    updated_cota = response.json()
    assert updated_cota["id"] == created_cota["id"]
    assert updated_cota["name"] == update_data["name"]
    assert updated_cota["amount"] == update_data["amount"]


def test_delete_cota():
    """
    Testa a exclusão de uma cota existente.
    """
    cota_data = {
        "name": "Cota D",
        "amount": 4000,
        "interest_rate": 4,
        "duration_months": 48
    }
    response = client.post("/cotas/", json=cota_data)
    assert response.status_code == 201
    created_cota = response.json()

    response = client.delete(f"/cotas/{created_cota['id']}")
    assert response.status_code == 204

    response = client.get(f"/cotas/{created_cota['id']}")
    assert response.status_code == 404


def test_list_cotas():
    """
    Testa a listagem de todas as cotas.
    """
    # Criando múltiplas cotas
    for i in range(3):
        cota_data = {
            "name": f"Cota {i}",
            "amount": 1000 * (i + 1),
            "interest_rate": 1 + i,
            "duration_months": 12 * (i + 1)
        }
        response = client.post("/cotas/", json=cota_data)
        assert response.status_code == 201

    # Testando a listagem
    response = client.get("/cotas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3  # Verifica se pelo menos 3 cotas foram criadas


def test_invalid_cota_creation():
    """
    Testa a criação de uma cota com dados inválidos.
    """
    invalid_data = {
        "name": "Cota Inválida",
        "amount": -1000,  # Valor inválido
        "interest_rate": -1,  # Taxa inválida
        "duration_months": 0  # Duração inválida
    }
    response = client.post("/cotas/", json=invalid_data)
    assert response.status_code == 422  # Espera erro de validação
    data = response.json()
    assert "detalhe" in data  # Verifica se a mensagem de erro está presente
    assert len(data["detalhe"]) > 0  # Verifica se há detalhes sobre os erros


def test_get_nonexistent_cota():
    """
    Testa a busca de uma cota inexistente.
    """
    response = client.get("/cotas/9999")  # ID inexistente
    assert response.status_code == 404
    data = response.json()
    assert data["detalhe"] == "Cota não encontrada."
    
def test_get_cota_profit():
    """
    Testa a busca do lucro de uma cota específica pelo ID.
    """
    # Criando uma cota para teste
    cota_data = {
        "name": "Cota Lucro",
        "amount": 1000.0,
        "interest_rate": 2.0,  # 2% ao mês
        "duration_months": 12  # 12 meses
    }
    response = client.post("/cotas/", json=cota_data)
    assert response.status_code == 201  # Verifica se a cota foi criada com sucesso
    created_cota = response.json()

    # Adicionando print para verificar a cota criada
    print(f"Cota criada: {created_cota}")

    # Extraindo o ID da cota criada
    cota_id = created_cota["id"]

    # Verificando se a cota existe no banco de dados
    response = client.get(f"/cotas/{cota_id}")
    assert response.status_code == 200  # Verifica se a cota foi encontrada
    print(f"Cota encontrada no banco de dados: {response.json()}")

    # Calculando o lucro esperado (juros simples)
    amount = cota_data["amount"]
    interest_rate = cota_data["interest_rate"]
    duration_months = cota_data["duration_months"]
    rendimento = amount * (interest_rate / 100) * duration_months
    gross_value = amount + rendimento
    tax = 0.15  # 15% de imposto
    net_value = gross_value - (rendimento * tax)

    # Fazendo a requisição para obter o lucro
    response = client.get(f"/cotas/cotas/{cota_id}/profit")  # Caminho corrigido
    print(f"Resposta do endpoint /profit: {response.status_code}, {response.json() if response.status_code == 200 else response.text}")
    assert response.status_code == 200  # Verifica se o endpoint retornou sucesso
    data = response.json()

    # Adicionando prints para depuração
    print(f"Dados retornados pelo endpoint: {data}")
    print(f"Valores calculados: gross_value={gross_value}, net_value={net_value}")

    # Verificando os valores retornados
    assert round(data["gross_value"], 2) == round(gross_value, 2)  # Comparação com arredondamento
    assert round(data["net_value"], 2) == round(net_value, 2)  # Comparação com arredondamento


def test_get_cota_profit_with_fixed_id():
    """
    Testa a busca do lucro e da rentabilidade de uma cota específica pelo ID fixo.
    """
    # ID fixo para o teste
    cota_id = 1

    # Dados esperados para a cota com ID fixo
    amount = 1000.0
    interest_rate = 2.0 / 100  # Convertendo para decimal
    duration_months = 12
    tax = 0.15  # 15% de imposto

    # Calculando os valores esperados
    profitability = amount * (interest_rate * 100) * duration_months  # Rentabilidade (juros simples)
    gross_value = amount + profitability  # Valor bruto
    net_value = gross_value - (profitability * tax)  # Valor líquido

    # Fazendo a requisição para obter o lucro
    response = client.get(f"/cotas/{cota_id}/profit")
    print(f"Resposta do endpoint /profit: {response.status_code}, {response.json() if response.status_code == 200 else response.text}")
    assert response.status_code == 200  # Verifica se o endpoint retornou sucesso
    data = response.json()

    # Adicionando prints para depuração
    print(f"Dados retornados pelo endpoint: {data}")
    print(f"Valores calculados: gross_value={gross_value}, net_value={net_value}, profitability={profitability}")

    # Verificando os valores retornados
    assert round(data["gross_value"], 2) == round(gross_value, 2)  # Comparação com arredondamento
    assert round(data["net_value"], 2) == round(net_value, 2)  # Comparação com arredondamento
    assert round(data["profitability"], 2) == round(profitability, 2)  # Verifica a rentabilidade
