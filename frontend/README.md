# Frontend  Interface Desktop

Interface gráfica do condoERP desenvolvida com **PySide6** (Qt para Python). Consome a API REST do backend e oferece uma aplicação desktop para gerenciamento do condomínio.

---

## Estrutura

```
frontend/
 app.py              # Ponto de entrada: inicializa o QApplication e abre a tela de login
 requirements.txt    # Dependências Python
 controller/         # Lógica de interface (conecta view e model)
    api.py          # Cliente HTTP centralizado para comunicação com o backend
    login.py        # Controla tela de login e cadastro
    home.py         # Controla a tela principal (home)
 model/              # Camada de dados (chama o ApiClient)
    login.py        # Autenticação e criação de conta
    home.py         # Encomendas, notificações, veículos, visitantes, ocorrências
 view/               # Arquivos de interface Qt Designer (.ui)
     login.ui        # Tela de login e cadastro
     home.ui         # Tela principal com abas
     addEncomenda.ui
     addNotificacao.ui
     addOcorrencia.ui
     addVeiculo.ui
     addVisitante.ui
```

---

## Instalação

```bash
cd frontend
pip install -r requirements.txt
```

### Dependências

```
PySide6
requests
```

---

## Execução

Certifique-se de que o **backend esteja rodando** antes de iniciar.

```bash
python app.py
```

---

## Configuração da API

O endereço do backend é definido em `controller/api.py`:

```python
BASE_URL = "http://10.28.0.127:5000"
TIMEOUT = 5  # segundos
```

Altere `BASE_URL` para o IP/host onde o backend está rodando.

---

## Arquitetura

O frontend segue o padrão **MVC (Model-View-Controller)**:

```
View (.ui)    Controller (.py)    Model (.py)    ApiClient    Backend
```

- **View**: arquivos `.ui` gerados no Qt Designer, carregados em tempo de execução com `QUiLoader`
- **Controller**: gerencia eventos de botões, validações de campo e navegação entre telas
- **Model**: chama o `ApiClient` e retorna os dados já tratados ao controller
- **ApiClient**: wrapper sobre `requests` com tratamento padronizado de erros e respostas

---

## ApiClient (`controller/api.py`)

Wrapper centralizado para todas as chamadas HTTP ao backend:

```python
ApiClient.get("/encomendas")
ApiClient.post("/login/auth", {"ilogin": "user", "senha": "123"})
ApiClient.put("/veiculos/1", {"placa": "ABC1234"})
ApiClient.delete("/ocorrencias/5")
```

Trata automaticamente erros de conexão, timeout e respostas não-JSON.

---

## Telas

### Login (`view/login.ui`)

Tela inicial com duas abas via `QStackedWidget`:

- **Aba 0  Login**: campos de usuário e senha, botão entrar
- **Aba 1  Cadastro**: nome, e-mail, telefone, CPF, data de nascimento, senha, confirmação e tipo de acesso (morador/visitante)

### Home (`view/home.ui`)

Tela principal após autenticação, com seções para:

-  Encomendas
-  Notificações
-  Veículos
-  Visitantes
-  Ocorrências

Cada seção possui formulários de adição (`.ui` separados) e listagem com opção de remoção.

---

## Validações

O controller de login realiza as seguintes validações antes de chamar a API:

- Campos obrigatórios não podem ser vazios
- Senha e confirmação de senha devem coincidir
- Tipo de acesso mapeado para `morador` ou `visitante`
