# Banco de Dados

Módulo responsável pela criação e configuração do banco de dados **MySQL** do condoERP.

---

## Estrutura

```
db/
 db.sql          # Script DDL completo (criação do banco e todas as tabelas)
 db.py           # Script Python para executar o db.sql via linha de comando
 requirements.txt
```

---

## Instalação

```bash
cd db
pip install -r requirements.txt
```

### Dependência

```
mysql-connector-python>=8.0.0
```

---

## Criação do Banco

```bash
python db.py --host localhost --user root --password sua_senha
```

Parâmetros disponíveis:

| Parâmetro    | Padrão      | Descrição              |
|--------------|-------------|------------------------|
| `--host`     | `localhost` | Host do MySQL          |
| `--user`     | `root`      | Usuário do MySQL       |
| `--password` | *(vazio)*   | Senha do MySQL         |
| `--port`     | `3306`      | Porta do MySQL         |
| `--sql`      | `./db.sql`  | Caminho do arquivo SQL |

Após a execução, o banco `sistema_condominio` estará criado com todas as tabelas.

---

## Diagrama de Tabelas

```
usuarios
   id, nome, idade, cpf (unique), telefone, data_nasc

 login
       id, id_user (FK), ilogin (unique), senha, tipo_acesso

 veiculos
       id, id_usuario (FK), placa, descricao, documento

 apartamentos
       id, numero, descricao

 estacionamento
       id, numero

 moradores
       id, id_user (FK), id_veiculo (FK), id_vaga (FK), id_apto (FK)

 visitantes
       id, id_user (FK), id_veiculo (FK), id_vaga (FK), id_morador (FK)

 funcionarios
       id, id_user (FK), id_veiculo (FK), id_vaga (FK), descricao

 encomendas
       id, id_usuario (FK), descricao, data_entrega, data_coleta

 ocorrencias
       id, id_usuario (FK), descricao

 notificacoes
        id, id_usuario (FK), descricao
```

---

## Descrição das Tabelas

### `usuarios`
Base de todos os usuários do sistema. Cada morador, visitante e funcionário é um usuário.

| Coluna      | Tipo           | Descrição                  |
|-------------|----------------|----------------------------|
| id          | INT PK AI      | Identificador único        |
| nome        | VARCHAR(255)   | Nome completo              |
| idade       | INT            | Idade                      |
| cpf         | VARCHAR(14)    | CPF (único no sistema)     |
| telefone    | VARCHAR(20)    | Telefone de contato        |
| data_nasc   | DATE           | Data de nascimento         |

---

### `login`
Credenciais de acesso vinculadas a um usuário.

| Coluna       | Tipo                                              | Descrição                     |
|--------------|---------------------------------------------------|-------------------------------|
| id           | INT PK AI                                         | Identificador                 |
| id_user      | INT FK  usuarios.id                              | Usuário dono do login         |
| ilogin       | VARCHAR(255) UNIQUE                               | Identificador de login (email)|
| senha        | VARCHAR(64)                                       | Senha em SHA-256              |
| tipo_acesso  | ENUM('morador','visitante','funcionario','admin') | Nível de acesso               |

---

### `apartamentos`
Unidades do condomínio.

| Coluna    | Tipo         | Descrição        |
|-----------|--------------|------------------|
| id        | INT PK AI    | Identificador    |
| numero    | INT          | Número do apto   |
| descricao | VARCHAR(255) | Observações      |

---

### `veiculos`
Veículos cadastrados por usuários.

| Coluna    | Tipo         | Descrição                      |
|-----------|--------------|--------------------------------|
| id        | INT PK AI    | Identificador                  |
| id_usuario| INT FK       | Usuário dono do veículo        |
| placa     | VARCHAR(10)  | Placa do veículo               |
| descricao | VARCHAR(255) | Modelo/cor/observações         |
| documento | VARCHAR(255) | Documento do veículo           |

---

### `estacionamento`
Vagas de estacionamento do condomínio.

| Coluna | Tipo      | Descrição             |
|--------|-----------|-----------------------|
| id     | INT PK AI | Identificador         |
| numero | INT       | Número da vaga        |

---

### `moradores`
Vínculo entre usuário, apartamento e vaga.

| Coluna     | Tipo      | Descrição                     |
|------------|-----------|-------------------------------|
| id         | INT PK AI | Identificador                 |
| id_user    | INT FK    | Usuário (morador)             |
| id_veiculo | INT FK    | Veículo do morador            |
| id_vaga    | INT FK    | Vaga de estacionamento        |
| id_apto    | INT FK    | Apartamento do morador        |

---

### `visitantes`
Registro de visitas ao condomínio.

| Coluna     | Tipo      | Descrição                      |
|------------|-----------|--------------------------------|
| id         | INT PK AI | Identificador                  |
| id_user    | INT FK    | Usuário visitante              |
| id_veiculo | INT FK    | Veículo utilizado              |
| id_vaga    | INT FK    | Vaga ocupada                   |
| id_morador | INT FK    | Morador visitado               |

---

### `funcionarios`
Funcionários vinculados ao sistema.

| Coluna     | Tipo         | Descrição                  |
|------------|--------------|----------------------------|
| id         | INT PK AI    | Identificador              |
| id_user    | INT FK       | Usuário funcionário        |
| id_veiculo | INT FK       | Veículo do funcionário     |
| id_vaga    | INT FK       | Vaga de estacionamento     |
| descricao  | VARCHAR(255) | Cargo/função               |

---

### `encomendas`

| Coluna       | Tipo         | Descrição                     |
|--------------|--------------|-------------------------------|
| id           | INT PK AI    | Identificador                 |
| id_usuario   | INT FK       | Morador destinatário          |
| descricao    | VARCHAR(255) | Descrição da encomenda        |
| data_entrega | DATE         | Data de chegada no condomínio |
| data_coleta  | DATE         | Data de retirada pelo morador |

---

### `ocorrencias`

| Coluna     | Tipo         | Descrição              |
|------------|--------------|------------------------|
| id         | INT PK AI    | Identificador          |
| id_usuario | INT FK       | Usuário que registrou  |
| descricao  | VARCHAR(255) | Descrição da ocorrência|

---

### `notificacoes`

| Coluna     | Tipo         | Descrição              |
|------------|--------------|------------------------|
| id         | INT PK AI    | Identificador          |
| id_usuario | INT FK       | Usuário destinatário   |
| descricao  | VARCHAR(255) | Conteúdo da notificação|
