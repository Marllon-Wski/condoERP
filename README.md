# condoERP  Sistema de Gerenciamento de Condomínio

Sistema completo para administração de condomínios, desenvolvido por **Marllon Wendrechowski** e **Antonio Neto**.

A aplicação é dividida em três módulos independentes: uma **API REST** em Flask, uma **interface desktop** em PySide6 e um **banco de dados** MySQL.

---

## Estrutura do Projeto

```
condoERP/
 backend/        # API REST (Flask + MySQL)
 frontend/       # Interface desktop (PySide6)
 db/             # Scripts do banco de dados (MySQL)
 backup/         # Versões anteriores do projeto
 README.md
```

---

## Tecnologias Utilizadas

| Camada     | Tecnologia                        |
|------------|-----------------------------------|
| Backend    | Python 3, Flask 3.0, MySQL        |
| Frontend   | Python 3, PySide6, Requests       |
| Banco      | MySQL, mysql-connector-python     |

---

## Como Rodar o Projeto

### Pré-requisitos

- Python 3.10+
- MySQL Server rodando localmente
- `pip` para instalação de dependências

### 1. Banco de Dados

```bash
cd db
pip install -r requirements.txt
python db.py --host localhost --user root --password sua_senha
```

Isso cria o banco `sistema_condominio` com todas as tabelas necessárias.

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
```

Configure as variáveis de ambiente no arquivo `.env`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=sistema_condominio
```

Inicie a API:

```bash
python api.py
```

A API estará disponível em `http://localhost:5000`.

### 3. Frontend

```bash
cd frontend
pip install -r requirements.txt
python app.py
```

> Certifique-se de que o backend esteja rodando antes de iniciar o frontend. O endereço da API é configurado em `frontend/controller/api.py` na variável `BASE_URL`.

---

## Funcionalidades

- **Autenticação** com controle de tipo de acesso (morador, visitante, funcionário, admin)
- **Gestão de Moradores** com vínculo a apartamentos e vagas
- **Gestão de Visitantes** com controle de entrada e morador vinculado
- **Gestão de Funcionários** com cargo e vaga de estacionamento
- **Controle de Apartamentos** e **Estacionamento**
- **Registro de Veículos** por usuário
- **Encomendas** com data de entrega e coleta
- **Ocorrências** registradas por morador/funcionário
- **Notificações** internas por usuário

---

## Documentação por Módulo

- [Backend  API REST](./backend/README.md)
- [Frontend  Interface Desktop](./frontend/README.md)
- [Banco de Dados](./db/README.md)
