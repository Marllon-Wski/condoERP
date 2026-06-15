

from flask import Flask, jsonify, request, abort
from mysql.connector import Error
from datetime import date

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
#  ENCOMENDAS
# ─────────────────────────────────────────────────────────

@app.route("/encomendas", methods=["GET"])
def listar_encomendas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT e.*, u.nome AS nome_usuario
           FROM encomendas e
           JOIN usuarios u ON u.id = e.id_usuario
           ORDER BY e.data_entrega DESC"""
    )
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/encomendas/<int:eid>", methods=["GET"])
def buscar_encomenda(eid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT e.*, u.nome AS nome_usuario
           FROM encomendas e
           JOIN usuarios u ON u.id = e.id_usuario
           WHERE e.id = %s""",
        (eid,),
    )
    row = cur.fetchone()
    result = row_to_dict(cur, row) if row else None
    cur.close()
    conn.close()
    if not row:
        return json_error("Encomenda não encontrada.", 404)
    return json_ok(result)


@app.route("/encomendas/usuario/<int:id_usuario>", methods=["GET"])
def encomendas_por_usuario(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT e.*, u.nome AS nome_usuario
           FROM encomendas e
           JOIN usuarios u ON u.id = e.id_usuario
           WHERE e.id_usuario = %s
           ORDER BY e.data_entrega DESC""",
        (id_usuario,),
    )
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/encomendas", methods=["POST"])
def criar_encomenda():
    body = request.get_json(silent=True) or {}
    for campo in ["id_usuario", "descricao", "data_entrega"]:
        if not body.get(campo):
            return json_error(f"Campo obrigatório ausente: {campo}")

    try:
        data_entrega = date.fromisoformat(body.get("data_entrega"))
        data_coleta = (
            date.fromisoformat(body.get("data_coleta")) if body.get(
                "data_coleta") else None
        )
    except ValueError:
        return json_error("Formato de data inválido. Use AAAA-MM-DD.")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO encomendas (id_usuario, descricao, data_entrega, data_coleta)
               VALUES (%s, %s, %s, %s)""",
            (body.get("id_usuario"), body.get(
                "descricao"), data_entrega, data_coleta),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao registrar encomenda: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Encomenda registrada com sucesso."})


@app.route("/encomendas/<int:eid>", methods=["PUT"])
def atualizar_encomenda(eid):
    body = request.get_json(silent=True) or {}
    campos = ["descricao", "data_entrega", "data_coleta"]
    updates = {k: body[k] for k in campos if k in body}
    if not updates:
        return json_error("Nenhum campo válido para atualizar.")

    # Valida datas se presentes
    for campo_data in ["data_entrega", "data_coleta"]:
        if campo_data in updates:
            try:
                updates[campo_data] = date.fromisoformat(updates[campo_data])
            except ValueError:
                return json_error(f"Formato inválido em {campo_data}. Use AAAA-MM-DD.")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    valores = list(updates.values()) + [eid]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE encomendas SET {set_clause} WHERE id = %s", valores
        )
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Encomenda não encontrada.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Encomenda atualizada com sucesso."})


@app.route("/encomendas/<int:eid>", methods=["DELETE"])
def deletar_encomenda(eid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM encomendas WHERE id = %s", (eid,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Encomenda não encontrada.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao remover encomenda: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Encomenda removida com sucesso."})
