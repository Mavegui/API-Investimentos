# Cotas de investimento API
Este projeto tem como objetivo desenvolver uma API em Python para gerenciar cotas de investimento e calcular a rentabilidade com juros simples.

Trata-se de um projeto proposto como teste prático de programação em Python, utilizando API, para a vaga de desenvolvedor Python júnior na empresa [Vitalis Invest](https://www.vitalisinvest.com.br/).

---

### **Resumo do Projeto**
Este projeto é voltado exclusivamente para o **desenvolvimento do Back-End** de uma aplicação que gerencia **cotas de investimento**. Ele inclui a criação de uma **API RESTful**, configuração do **banco de dados**, documentação automática e implementação de **endpoints** para operações CRUD e cálculos financeiros.

---

### **Objetivo**


Fornecer uma API robusta e bem documentada para:

- **Gerenciar cotas de investimento** (criação, leitura, atualização, listagem e exclusão).
- **Calcular rentabilidade** e lucro com base em juros simples.
- **Facilitar a integração com sistemas Front-End** ou outras aplicações.

---

### **Principais Componentes**

1. **API RESTful:**
   - Desenvolvida com **FastAPI**, garantindo alta performance e facilidade de uso.
   - Endpoints bem definidos para operações CRUD e cálculos financeiros.

2. **Banco de Dados:**
   - Configurado com **SQLAlchemy** para gerenciar as cotas de investimento.
   - Suporte a operações como criação, leitura, atualização e exclusão de registros.

3. **Documentação Automática:**
   - Gerada automaticamente pelo **Swagger UI**, acessível em `/docs`.
   - Permite explorar e testar os endpoints diretamente no navegador.

4. **Endpoints Implementados:**
   - **`POST /cotas/`**: Criar uma nova cota.
   - **`GET /cotas/`**: Listar todas as cotas com paginação.
   - **`GET /cotas/{cota_id}`**: Buscar uma cota específica pelo ID.
   - **`PUT /cotas/{cota_id}`**: Atualizar uma cota existente.
   - **`DELETE /cotas/{cota_id}`**: Deletar uma cota pelo ID.
   - **`GET /cotas/{cota_id}/profit`**: Calcular o lucro bruto, líquido e a rentabilidade de uma cota.

5. **Testes Automatizados:**
   - Implementados com **pytest** para garantir a qualidade e confiabilidade do Back-End.

6. **Containerização:**
   - O projeto é totalmente containerizado com **Docker**, facilitando a implantação e execução em diferentes ambientes.

---

### **Tecnologias Utilizadas**
- **FastAPI**: Framework para criação da API.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **Pydantic**: Validação e serialização de dados.
- **Docker**: Para containerização e fácil implantação.
- **pytest**: Para testes automatizados.
- **Banco de dados**: SQLite3

---

## Como Rodar o Projeto

1. Clone o repositório:

   ```bash
   git clone https://github.com/Mavegui/API-Investimentos.git
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Crie e inicialize o banco de dados:

   ```bash
   # No terminal
   python -m app.create_db

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
- **GET /cotas/{cota_id}/profit**: Mostra os dados que são calculados.

---

## Usando a Imagem do Docker Hub

A imagem deste projeto está disponível no Docker Hub. Para utilizá-la, siga os passos abaixo:

1. **Baixe a imagem do Docker Hub**:

   ```bash
   docker pull mavegui/api-investimentos:latest
   ```

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
|   ├── create_db.py             # Ponto de criar banco
│   └── main.py                  # Ponto de entrada da aplicação
├── Dockerfile                   # Configuração do Docker
├── requirements.txt             # Dependências do projeto
├── .gitignore                   # Dependências ignoradas
└── README.md                    # Documentação do projeto
```
