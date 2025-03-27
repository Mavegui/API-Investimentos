# Cotas de investimento API

Este projeto tem como objetivo desenvolver uma API em Python para controlar cotas de investimento e calcular a rentabilidade com juros simples.

Trata-se de um projeto proposto como teste prático de programação em Python, utilizando API, para a vaga de desenvolvedor Python júnior na empresa [Vitalis Invest](https://www.vitalisinvest.com.br/).

## Tecnologias Usadas
- **Python 3.12+**
- **FastAPI** - Para a criação da API
- **SQLAlchemy** - Para comunicação com o banco de dados
- **SQLite** - Banco utilizado no projeto
- **Pydantic** - Para validação de dados
- **Pytest** - Para realizar testes de endpoints
- **Docker** - Projeto com suporte a containerização
- **Docker Hub** - Imagem armazenada no Docker Hub

---

## Como Rodar o Projeto

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Crie e inicialize o banco de dados:

   ```bash
   # No terminal
   python -m app.nomeDatabase

4. Execute o servidor da API:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Acesse a documentação automática do Swagger UI:

   ```
   http://127.0.0.1:8000/docs
   ```

---

## Endpoints

- **GET /cotas**: Lista todas as cotas.
- **POST /cotas**: Cria uma nova cota.
- **GET /cotas/{cota_id}**: Obtém os detalhes de uma cota específica.
- **PUT /cotas/{cota_id}**: Atualiza uma cota existente.
- **DELETE /cotas/{cota_id}**: Deleta uma cota.
- **GET /cotas/{cota_id}/profit**: Mostra o dados que são calculados.

---

## Usando a Imagem do Docker Hub

A imagem deste projeto está disponível no Docker Hub. Para utilizá-la, siga os passos abaixo:

1. **Baixe a imagem do Docker Hub**:

   ```bash
   docker pull mavegui/api-investimentos:latest
   ```

---

## Docker

O projeto pode ser executado dentro de um container Docker. Para isso, siga os passos abaixo:

1. **Construa a imagem Docker**:

   ```bash
   docker build -t cotas-investimento-api .
   ```

2. **Execute o container**:

   ```bash
   docker run -d -p 8000:8000 cotas-investimento-api
   ```

3. **Acesse a API**:

   - Acesse a documentação do Swagger UI em:
     ```
     http://127.0.0.1:8000/docs
     ```

---

## Rodando os Testes

Para rodar os testes automatizados, utilize o comando abaixo:

```bash
pytest
```

Se quiser um relatório mais detalhado, use:

```bash
pytest -v
```

---

## Estrutura do Projeto

```plaintext
.
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   └── cotas_routes.py  # Rotas da API
│   ├── crud/
│   │   └── crud.py              # Operações de banco de dados
│   ├── database/
│   │   ├── database.py          # Configuração do banco de dados
│   ├── models/
│   │   └── cota_model.py        # Modelos do banco de dados
│   ├── schemas/
│   │   └── schemas.py           # Esquemas de validação
│   ├── tests/
│   │   └── test_main.py         # Testes automatizados
│   └── main.py                  # Ponto de entrada da aplicação
├── Dockerfile                   # Configuração do Docker
├── requirements.txt             # Dependências do projeto
└── README.md                    # Documentação do projeto
```
