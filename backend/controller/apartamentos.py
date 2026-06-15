

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
#  APARTAMENTOS
# ─────────────────────────────────────────────────────────

@app.route("/apartamentos", methods=["GET"])
def listar_apartamentos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apartamentos ORDER BY numero")
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/apartamentos/<int:aid>", methods=["GET"])
def buscar_apartamento(aid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM apartamentos WHERE id = %s", (aid,))
    row = cur.fetchone()
    result = row_to_dict(cur, row) if row else None
    cur.close()
    conn.close()
    if not row:
        return json_error("Apartamento não encontrado.", 404)
    return json_ok(result)


@app.route("/apartamentos", methods=["POST"])
def criar_apartamento():
    body = request.get_json(silent=True) or {}
    if body.get("numero") is None:
        return json_error("Campo obrigatório ausente: numero")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO apartamentos (numero, descricao) VALUES (%s, %s)",
            (body["numero"], body.get("descricao")),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao criar apartamento: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Apartamento cadastrado com sucesso."})


@app.route("/apartamentos/<int:aid>", methods=["PUT"])
def atualizar_apartamento(aid):
    body = request.get_json(silent=True) or {}
    campos = ["numero", "descricao"]
    updates = {k: body[k] for k in campos if k in body}
    if not updates:
        return json_error("Nenhum campo válido para atualizar.")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    valores = list(updates.values()) + [aid]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE apartamentos SET {set_clause} WHERE id = %s", valores
        )
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Apartamento não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Apartamento atualizado com sucesso."})


@app.route("/apartamentos/<int:aid>", methods=["DELETE"])
def deletar_apartamento(aid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM apartamentos WHERE id = %s", (aid,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Apartamento não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(
            "Não é possível excluir: apartamento possui moradores vinculados.", 409
        )
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Apartamento removido com sucesso."})
