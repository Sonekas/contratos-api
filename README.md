# API de Contratos Públicos - Entrega 1

Este projeto implementa uma API RESTful utilizando FastAPI, SQLAlchemy e SQLite, com autenticação JWT, para gerir dados de contratos públicos. Os dados foram obtidos do portal dados.gov.br.

## Estrutura do Projeto

```
contratos_api/
├── src/
│   ├── database.py         # Configuração da base de dados
│   ├── main.py             # Ponto de entrada da aplicação FastAPI
│   ├── models/             # Modelos SQLAlchemy (Fornecedor, Contrato, Usuario)
│   │   ├── __init__.py
│   │   ├── contrato.py
│   │   ├── fornecedor.py
│   │   └── usuario.py
│   ├── routes/             # Rotas da API (Autenticação, Fornecedores, Contratos)
│   │   ├── auth.py
│   │   ├── contratos.py
│   │   └── fornecedores.py
│   ├── schemas.py          # Schemas Pydantic para validação de dados
│   └── auth.py             # Funções de autenticação JWT e hash de senha
├── populate_db.py          # Script para popular a base de dados
├── Contratos_API_Postman_Collection.json # Coleção Postman para testes
├── README.md               # Este ficheiro
├── data_modeling.md        # Documentação da modelagem de dados
├── er_diagram.png          # Diagrama Entidade-Relacionamento
└── venv/                   # Ambiente virtual Python
```

## Como Executar Localmente

Siga os passos abaixo para configurar e executar a API no seu ambiente local:

### 1. Pré-requisitos

Certifique-se de ter o Python 3.8+ e `pip` instalados.

### 2. Clonar o Repositório

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd contratos_api
```

### 3. Configurar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

**Nota:** O ficheiro `requirements.txt` será gerado após a instalação das dependências. Certifique-se de que ele está atualizado.

### 4. Popular a Base de Dados

Execute o script de população para criar as tabelas e inserir dados iniciais, incluindo utilizadores `admin` e `leitor`.

```bash
python populate_db.py
```

**Credenciais Padrão:**
- **Admin:** `username: admin`, `password: admin123`
- **Leitor:** `username: leitor`, `password: leitor123`

### 5. Iniciar a API

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 5000
```

A API estará disponível em `http://localhost:5000`.

### 6. Aceder à Documentação Interativa

Após iniciar a API, pode aceder à documentação interativa do Swagger UI em:

- [http://localhost:5000/docs](http://localhost:5000/docs)
- [http://localhost:5000/redoc](http://localhost:5000/redoc)

## Testes com Postman

Uma coleção Postman (`Contratos_API_Postman_Collection.json`) é fornecida para facilitar os testes dos endpoints. Importe-a para o Postman e configure a variável de ambiente `base_url` para `http://localhost:5000`.

Os testes incluem:
- Registo e Login de utilizadores.
- Obtenção de token JWT.
- Operações CRUD para Fornecedores (protegidas por autenticação e autorização de admin).
- Operações CRUD para Contratos (protegidas por autenticação e autorização de admin).

## Modelagem de Dados

Consulte `data_modeling.md` e `er_diagram.png` para detalhes sobre a modelagem de dados e o diagrama Entidade-Relacionamento.

## Contribuição

Este projeto segue o padrão Git Flow. As contribuições devem ser feitas através de branches de feature e pull requests para a branch `develop`.

## Licença

[Adicionar informações de licença, se aplicável]
