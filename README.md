# condoERP — Sistema de Gerenciamento de Condomínio

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8-4479A1?logo=mysql&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Qt-41CD52?logo=qt&logoColor=white)

Sistema para administração de condomínios: moradores, visitantes, funcionários, vagas de garagem, veículos, encomendas, ocorrências e notificações. Desenvolvido por **Marllon Wendrechowski** e **Antonio Neto**.

O projeto é dividido em três camadas independentes que conversam por HTTP:

```
┌────────────────────┐   HTTP/JSON   ┌────────────────────┐   SQL   ┌──────────────┐
│ Frontend desktop   │ ────────────► │ API REST (Flask)   │ ──────► │ MySQL        │
│ PySide6 (Qt)       │ ◄──────────── │ 11 módulos de rota │ ◄────── │ 11 tabelas   │
└────────────────────┘               └────────────────────┘         └──────────────┘
```

---

## Destaques técnicos

- **API REST com mais de 60 endpoints** de CRUD, organizados em um módulo por entidade (`backend/controller/`).
- **Autenticação** por login e senha (`POST /login/auth`), com senha armazenada como hash SHA-256 e **controle de acesso por tipo de usuário** (morador, visitante, funcionário, admin).
- **Respostas JSON padronizadas** e tratamento global de erros (404, 405, 503) via helpers em `backend/utils/helpers.py`.
- **Health check** (`GET /health`) que testa a conexão com o banco e responde 503 quando ele cai.
- **Modelo relacional** com 11 tabelas e chaves estrangeiras (`db/db.sql`), criado automaticamente por script.
- **Interface desktop** com telas desenhadas no Qt Designer (`frontend/view/*.ui`), separadas em model, view e controller.
- Configuração por **variáveis de ambiente** (`.env`) e logging na API.

---

## Funcionalidades

| Módulo | O que faz |
|---|---|
| Usuários e login | Cadastro de usuários e credenciais, autenticação e tipo de acesso |
| Moradores | Vínculo do morador ao apartamento, veículo e vaga |
| Visitantes | Registro de entrada com morador responsável e vaga |
| Funcionários | Cadastro com cargo, veículo e vaga |
| Apartamentos | Cadastro e manutenção das unidades |
| Estacionamento | Vagas, incluindo consulta de vagas livres (`GET /estacionamento/disponiveis`) |
| Veículos | Veículos por usuário |
| Encomendas | Data de chegada e de retirada, por morador |
| Ocorrências | Registro e acompanhamento de ocorrências |
| Notificações | Mensagens internas por usuário |

A lista completa de rotas está no topo de [`backend/api.py`](./backend/api.py) e no [README do backend](./backend/README.md).

---

## Estrutura do projeto

```
condoERP/
├── backend/        # API REST (Flask + MySQL)
│   ├── api.py          # ponto de entrada e rotas utilitárias
│   ├── config.py       # app Flask, configuração do banco e logging
│   ├── controller/     # um módulo de rotas por entidade
│   └── utils/          # conexão, serialização e respostas JSON
├── frontend/       # Interface desktop (PySide6)
│   ├── app.py
│   ├── controller/ model/ view/
├── db/             # Script de criação do banco (db.py + db.sql)
└── backup/         # Versões anteriores
```

---

## Como rodar

### Pré-requisitos

- Python 3.10+
- MySQL Server 8 rodando localmente

> Os módulos importam o pacote como `condoERP.…`, então os comandos de execução abaixo rodam **a partir da pasta que contém o repositório** (a pasta acima de `condoERP/`).

### 1. Banco de dados

```bash
pip install -r condoERP/db/requirements.txt
python condoERP/db/db.py --host localhost --user root --password sua_senha
```

Isso cria o banco `sistema_condominio` com todas as tabelas.

### 2. API

```bash
pip install -r condoERP/backend/requirements.txt
```

Crie `condoERP/backend/.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=sistema_condominio
PORT=5000
FLASK_DEBUG=false
```

Inicie:

```bash
python -m condoERP.backend.api
```

Teste com `curl http://localhost:5000/health`.

### 3. Interface desktop

Ajuste `BASE_URL` em `condoERP/frontend/controller/api.py` para o endereço da sua API (ex.: `http://localhost:5000`) e rode:

```bash
pip install -r condoERP/frontend/requirements.txt
python -m condoERP.frontend.app
```

---

## Exemplo de uso da API

```bash
# Autenticar
curl -X POST http://localhost:5000/login/auth \
  -H "Content-Type: application/json" \
  -d '{"ilogin": "admin", "senha": "sua_senha"}'

# Listar vagas livres
curl http://localhost:5000/estacionamento/disponiveis
```

---

## Próximos passos

- [ ] Testes automatizados da API com `pytest`
- [ ] Docker Compose (API + MySQL) para subir tudo com um comando
- [ ] Autenticação por token (JWT) e hash de senha com salt (bcrypt)
- [ ] Documentação interativa (Swagger/OpenAPI)
- [ ] Deploy da API em nuvem

---

## Documentação por módulo

- [Backend — API REST](./backend/README.md)
- [Frontend — Interface desktop](./frontend/README.md)
- [Banco de dados](./db/README.md)

## Autores

- **Marllon Wendrechowski** — [github.com/Marllon-Wski](https://github.com/Marllon-Wski)
- **Antonio Neto**
