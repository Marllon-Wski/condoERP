

import os
from dotenv import load_dotenv
from flask import Flask
import logging

# ── Configuração de Logging ───────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
logger = logging.getLogger(__name__)

# ── Aplicação Flask (instância compartilhada) ─────────────
# Todos os módulos em backend/models/*.py importam este `app`
# e registram suas rotas nele via @app.route(...)
app = Flask(__name__)
app.config["JSON_ENSURE_ASCII"] = False

# ── Configuração do Banco de Dados ────────────────────────
load_dotenv()
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER",     "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME",     "db")
}
