# --------------------
#  SISTEMA DE GERENCIAMENTO DE CONDOMÍNIO — API REST
#  Framework : Flask
#  Banco     : MySQL
# --------------------
# Rotas disponíveis
# ─────────────────────────────────────────────────────────
#  USUÁRIOS
#   GET    /usuarios                        → lista todos
#   GET    /usuarios/<id>                   → busca por ID
#   POST   /usuarios                        → cadastra novo (tipo: visitante/morador/funcionário)
#   PUT    /usuarios/<id>                   → atualiza
#   DELETE /usuarios/<id>                   → remove
#
#  MORADORES
#   GET    /moradores                       → lista todos
#   GET    /moradores/<id_usuario>          → busca por ID de usuário
#   POST   /moradores                       → vincula morador a apartamento e veículo/vaga
#   PUT    /moradores/<id_usuario>          → atualiza dados (apto, veículo, vaga)
#   DELETE /moradores/<id_usuario>          → remove vínculo
#
#  VISITANTES
#   GET    /visitantes                      → lista todos
#   GET    /visitantes/<id_vaga>            → busca por vaga
#   POST   /visitantes                      → registra entrada de visitante
#   PUT    /visitantes/<id_vaga>            → atualiza dados (veículo, morador vinculado)
#   DELETE /visitantes/<id_vaga>            → remove registro
#
#  FUNCIONÁRIOS
#   GET    /funcionarios                    → lista todos
#   GET    /funcionarios/<id_usuario>       → busca por ID de usuário
#   POST   /funcionarios                    → cadastra funcionário com vaga/veículo
#   PUT    /funcionarios/<id_usuario>       → atualiza dados
#   DELETE /funcionarios/<id_usuario>       → remove
#
#  APARTAMENTOS
#   GET    /apartamentos                    → lista todos
#   GET    /apartamentos/<id>               → busca por ID
#   POST   /apartamentos                    → cadastra novo
#   PUT    /apartamentos/<id>               → atualiza
#   DELETE /apartamentos/<id>              → remove
#
#  VEÍCULOS
#   GET    /veiculos                        → lista todos
#   GET    /veiculos/<id>                   → busca por ID
#   GET    /veiculos/usuario/<id_usuario>   → lista veículos de um usuário
#   POST   /veiculos                        → cadastra novo veículo
#   PUT    /veiculos/<id>                   → atualiza
#   DELETE /veiculos/<id>                   → remove
#
#  ESTACIONAMENTO
#   GET    /estacionamento                  → lista todas as vagas
#   GET    /estacionamento/<id>             → busca vaga por ID
#   GET    /estacionamento/disponiveis      → lista vagas livres
#   POST   /estacionamento                  → cadastra nova vaga
#   PUT    /estacionamento/<id>             → atualiza dados da vaga
#   DELETE /estacionamento/<id>             → remove vaga
#
#  ENCOMENDAS
#   GET    /encomendas                      → lista todas
#   GET    /encomendas/<id>                 → busca por ID
#   GET    /encomendas/usuario/<id_usuario> → encomendas de um morador
#   POST   /encomendas                      → registra nova encomenda
#   PUT    /encomendas/<id>                 → atualiza (ex: marcar como retirada)
#   DELETE /encomendas/<id>                 → remove registro
#
#  OCORRÊNCIAS
#   GET    /ocorrencias                     → lista todas
#   GET    /ocorrencias/<id>                → busca por ID
#   GET    /ocorrencias/usuario/<id_usuario>→ ocorrências de um usuário
#   POST   /ocorrencias                     → registra nova ocorrência
#   PUT    /ocorrencias/<id>                → atualiza descrição/status
#   DELETE /ocorrencias/<id>                → remove
#
#  NOTIFICAÇÕESS
#   GET    /notificacoes                        → lista todas
#   GET    /notificacoes/<id>                   → busca por ID
#   GET    /notificacoes/usuario/<id_usuario>   → notificações de um usuário
#   POST   /notificacoes                        → envia nova notificação
#   DELETE /notificacoes/<id>                   → remove
#
#  UTILITÁRIOS
#   GET    /health                          → status da API
# --------------------

from condoERP.backend.controller import apartamentos, encomendas, estacionamento, funcionarios, login, moradores, notificacoes, ocorrencias, usuarios, veiculos
from flask import jsonify, request, abort
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import date, datetime
from decimal import Decimal
import logging

from condoERP.backend.config import app, DB_CONFIG, logger
from condoERP.backend.utils.helpers import (
    get_connection,
    serialize,
    row_to_dict,
    rows_to_list,
    json_ok,
    json_created,
    json_error
)

# ── Importa os módulos de rotas ───────────────────────────
# Cada módulo abaixo registra suas próprias rotas em `app`
# através do decorator @app.route. O import precisa acontecer
# para que essas rotas sejam efetivamente registradas.
from condoERP.backend.controller import (  # noqa: E402,F401
    visitantes,
)


# ─────────────────────────────────────────────────────────
#  UTILITÁRIOS
# ─────────────────────────────────────────────────────────


@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_connection()
        conn.ping(reconnect=False)
        conn.close()
        db_ok = True
    except Exception:
        db_ok = False

    return jsonify({
        "api":    "ok",
        "banco":  "conectado" if db_ok else "falha",
        "versao": "1.0.0",
    }), 200 if db_ok else 503

# ── Tratamento de erros globais ───────────────────────────


@app.errorhandler(404)
def not_found(e):
    return json_error("Rota não encontrada.", 404)


@app.errorhandler(405)
def method_not_allowed(e):
    return json_error("Método HTTP não permitido.", 405)


@app.errorhandler(503)
def service_unavailable(e):
    return json_error(str(e.description), 503)

# ── Entrada ───────────────────────────────────────────────


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    logger.info("API iniciada em http://0.0.0.0:%s", port)
    app.run(host="0.0.0.0", port=port, debug=debug)
