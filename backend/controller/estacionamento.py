
from flask import Flask, jsonify, request, abort
from mysql.connector import Error

from condoERP.backend.config import app, logger, DB_CONFIG
from condoERP.backend.utils.helpers import (
    get_connection,
    serialize,
    row_to_dict,
    rows_to_list,
    json_ok,
    json_created,
    json_error
)


# ─────────────────────────────────────────────────────────
#  ESTACIONAMENTO
# ─────────────────────────────────────────────────────────

@app.route("/estacionamento", methods=["GET"])
def listar_vagas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM estacionamento ORDER BY numero")
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/estacionamento/disponiveis", methods=["GET"])
def vagas_disponiveis():
    # Vagas que não estão atribuídas a moradores, visitantes ou funcionários
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT e.*
           FROM estacionamento e
           WHERE e.id NOT IN (
               SELECT id_vaga FROM moradores    WHERE id_vaga IS NOT NULL
               UNION ALL
               SELECT id_vaga FROM visitantes   WHERE id_vaga IS NOT NULL
               UNION ALL
               SELECT id_vaga FROM funcionarios WHERE id_vaga IS NOT NULL
           )
           ORDER BY e.numero"""
    )
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/estacionamento/<int:eid>", methods=["GET"])
def buscar_vaga(eid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM estacionamento WHERE id = %s", (eid,))
        row = cur.fetchone()
        if not row:
            return json_error("Vaga não encontrada.", 404)
        result = row_to_dict(cur, row)
    finally:
        cur.close()
        conn.close()

    return json_ok(result)


@app.route("/estacionamento", methods=["POST"])
def criar_vaga():
    body = request.get_json(silent=True) or {}
    if body.get("numero") is None:
        return json_error("Campo obrigatório ausente: numero")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO estacionamento (numero) VALUES (%s)",
            (body["numero"],),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao criar vaga: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Vaga cadastrada com sucesso."})


@app.route("/estacionamento/<int:eid>", methods=["PUT"])
def atualizar_vaga(eid):
    body = request.get_json(silent=True) or {}
    if body.get("numero") is None:
        return json_error("Campo obrigatório ausente: numero")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE estacionamento SET numero = %s WHERE id = %s",
            (body["numero"], eid),
        )
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Vaga não encontrada.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Vaga atualizada com sucesso."})


@app.route("/estacionamento/<int:eid>", methods=["DELETE"])
def deletar_vaga(eid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM estacionamento WHERE id = %s", (eid,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Vaga não encontrada.", 404)
    except Error as e:
        conn.rollback()
        return json_error(
            "Não é possível excluir: vaga está vinculada a um morador/visitante/funcionário.", 409
        )
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Vaga removida com sucesso."})
