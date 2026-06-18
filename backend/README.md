# Backend  API REST

API REST do condoERP, construída com **Flask** e **MySQL**. Responsável por toda a lógica de negócio e persistência de dados do sistema de condomínio.

---

## Estrutura

```
backend/
 api.py              # Ponto de entrada da aplicação, registra as rotas e erros globais
 config.py           # Instância do Flask, configuração do banco e logging
 .env                # Variáveis de ambiente (não versionar em produção)
 requirements.txt    # Dependências Python
 controller/         # Módulos de rotas (um por entidade)
    apartamentos.py
    encomendas.py
    estacionamento.py
    funcionarios.py
    login.py
    moradores.py
    notificacoes.py
    ocorrencias.py
    usuarios.py
    veiculos.py
    visitantes.py
 utils/
     helpers.py      # Funções utilitárias: conexão, serialização, respostas JSON
```

---

## Instalação

```bash
cd backend
pip install -r requirements.txt
```

### Dependências

```
flask==3.0.3
mysql-connector-python==8.4.0
python-dotenv==1.1.1
hashlib
```

---

## Configuração

Edite o arquivo `.env` na raiz do backend:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=sistema_condominio
```

---

## Execução

```bash
python api.py
```

Porta padrão: **5000**. Pode ser alterada com a variável de ambiente `PORT`.  
Para modo debug: `FLASK_DEBUG=true`.

---

## Endpoints da API

Todas as respostas seguem o padrão:

```json
{ "sucesso": true,  "dados": { ... } }   // sucesso
{ "sucesso": false, "erro": "mensagem" }  // erro
```

### Login / Autenticação

| Método | Rota            | Descrição                          |
|--------|-----------------|------------------------------------|
| GET    | `/login`        | Lista todos os logins              |
| GET    | `/login/<id>`   | Busca login por ID                 |
| POST   | `/login`        | Cria novo usuário + login          |
| PUT    | `/login/<id>`   | Atualiza nome ou senha             |
| DELETE | `/login/<id>`   | Remove login                       |
| POST   | `/login/auth`   | Autentica (retorna tipo de acesso) |

**Payload de autenticação:**
```json
{ "ilogin": "usuario@email.com", "senha": "123456" }
```

**Resposta de sucesso:**
```json
{ "sucesso": true, "dados": { "id_user": 1, "tipo_acesso": "morador" } }
```

---

### Usuários

| Método | Rota              | Descrição        |
|--------|-------------------|------------------|
| GET    | `/usuarios`       | Lista todos      |
| GET    | `/usuarios/<id>`  | Busca por ID     |
| POST   | `/usuarios`       | Cadastra novo    |
| PUT    | `/usuarios/<id>`  | Atualiza         |
| DELETE | `/usuarios/<id>`  | Remove           |

---

### Moradores

| Método | Rota                    | Descrição                           |
|--------|-------------------------|-------------------------------------|
| GET    | `/moradores`            | Lista todos (com apto e dados)      |
| GET    | `/moradores/<id_user>`  | Busca por ID de usuário             |
| POST   | `/moradores`            | Vincula morador a apartamento/vaga  |
| PUT    | `/moradores/<id_user>`  | Atualiza vínculo                    |
| DELETE | `/moradores/<id_user>`  | Remove vínculo                      |

---

### Visitantes

| Método | Rota                     | Descrição                      |
|--------|--------------------------|--------------------------------|
| GET    | `/visitantes`            | Lista todos                    |
| GET    | `/visitantes/<id_vaga>`  | Busca por vaga                 |
| POST   | `/visitantes`            | Registra entrada de visitante  |
| PUT    | `/visitantes/<id_vaga>`  | Atualiza dados                 |
| DELETE | `/visitantes/<id_vaga>`  | Remove registro                |

---

### Funcionários

| Método | Rota                       | Descrição     |
|--------|----------------------------|---------------|
| GET    | `/funcionarios`            | Lista todos   |
| GET    | `/funcionarios/<id_user>`  | Busca por ID  |
| POST   | `/funcionarios`            | Cadastra      |
| PUT    | `/funcionarios/<id_user>`  | Atualiza      |
| DELETE | `/funcionarios/<id_user>`  | Remove        |

---

### Apartamentos

| Método | Rota                   | Descrição     |
|--------|------------------------|---------------|
| GET    | `/apartamentos`        | Lista todos   |
| GET    | `/apartamentos/<id>`   | Busca por ID  |
| POST   | `/apartamentos`        | Cadastra      |
| PUT    | `/apartamentos/<id>`   | Atualiza      |
| DELETE | `/apartamentos/<id>`   | Remove        |

---

### Veículos

| Método | Rota                            | Descrição                  |
|--------|---------------------------------|----------------------------|
| GET    | `/veiculos`                     | Lista todos                |
| GET    | `/veiculos/<id>`                | Busca por ID               |
| GET    | `/veiculos/usuario/<id_user>`   | Lista veículos de usuário  |
| POST   | `/veiculos`                     | Cadastra novo veículo      |
| PUT    | `/veiculos/<id>`                | Atualiza                   |
| DELETE | `/veiculos/<id>`                | Remove                     |

---

### Estacionamento

| Método | Rota                             | Descrição              |
|--------|----------------------------------|------------------------|
| GET    | `/estacionamento`                | Lista todas as vagas   |
| GET    | `/estacionamento/<id>`           | Busca vaga por ID      |
| GET    | `/estacionamento/disponiveis`    | Lista vagas livres     |
| POST   | `/estacionamento`                | Cadastra nova vaga     |
| PUT    | `/estacionamento/<id>`           | Atualiza               |
| DELETE | `/estacionamento/<id>`           | Remove                 |

---

### Encomendas

| Método | Rota                              | Descrição                     |
|--------|-----------------------------------|-------------------------------|
| GET    | `/encomendas`                     | Lista todas                   |
| GET    | `/encomendas/<id>`                | Busca por ID                  |
| GET    | `/encomendas/usuario/<id_user>`   | Encomendas de um morador      |
| POST   | `/encomendas`                     | Registra nova encomenda       |
| PUT    | `/encomendas/<id>`                | Atualiza (ex: marcar retirada)|
| DELETE | `/encomendas/<id>`                | Remove                        |

---

### Ocorrências

| Método | Rota                               | Descrição              |
|--------|------------------------------------|------------------------|
| GET    | `/ocorrencias`                     | Lista todas            |
| GET    | `/ocorrencias/<id>`                | Busca por ID           |
| GET    | `/ocorrencias/usuario/<id_user>`   | Ocorrências de usuário |
| POST   | `/ocorrencias`                     | Registra ocorrência    |
| PUT    | `/ocorrencias/<id>`                | Atualiza               |
| DELETE | `/ocorrencias/<id>`                | Remove                 |

---

### Notificações

| Método | Rota                                 | Descrição                 |
|--------|--------------------------------------|---------------------------|
| GET    | `/notificacoes`                      | Lista todas               |
| GET    | `/notificacoes/<id>`                 | Busca por ID              |
| GET    | `/notificacoes/usuario/<id_user>`    | Notificações de usuário   |
| POST   | `/notificacoes`                      | Envia nova notificação    |
| DELETE | `/notificacoes/<id>`                 | Remove                    |

---

### Utilitários

| Método | Rota       | Descrição                            |
|--------|------------|--------------------------------------|
| GET    | `/health`  | Status da API e conexão com o banco  |

---

## Segurança

- Senhas armazenadas com hash **SHA-256** via `hashlib`
- Validação de **CPF** com dígitos verificadores
- Controle de acesso por `tipo_acesso`: `morador`, `visitante`, `funcionario`, `admin`

---

## Utilitários (`utils/helpers.py`)

| Função              | Descrição                                       |
|---------------------|-------------------------------------------------|
| `get_connection()`  | Abre conexão com o MySQL (abort 503 em falha)   |
| `serialize(obj)`    | Converte `date`, `datetime` e `Decimal` p/ JSON |
| `row_to_dict()`     | Linha do cursor  dicionário                    |
| `rows_to_list()`    | Todas as linhas  lista de dicionários          |
| `json_ok()`         | Resposta 200 padronizada                        |
| `json_created()`    | Resposta 201 padronizada                        |
| `json_error()`      | Resposta de erro padronizada                    |
| `encriptar_senha()` | SHA-256 da senha                                |
| `validar_cpf()`     | Validação completa de CPF                       |
