
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
#  NOTIFICAÇÕES
# ─────────────────────────────────────────────────────────

@app.route("/notificacoes", methods=["GET"])
def listar_notificacoes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT n.*, u.nome AS nome_usuario
           FROM notificacoes n
           JOIN usuarios u ON u.id = n.id_usuario
           ORDER BY n.id DESC"""
    )
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/notificacoes/<int:nid>", methods=["GET"])
def buscar_notificacao(nid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT n.*, u.nome AS nome_usuario
           FROM notificacoes n
           JOIN usuarios u ON u.id = n.id_usuario
           WHERE n.id = %s""",
        (nid,),
    )
    row = cur.fetchone()
    result = row_to_dict(cur, row) if row else None
    cur.close()
    conn.close()
    if not row:
        return json_error("Notificação não encontrada.", 404)
    return json_ok(result)


@app.route("/notificacoes/usuario/<int:id_usuario>", methods=["GET"])
def notificacoes_por_usuario(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT n.*, u.nome AS nome_usuario
           FROM notificacoes n
           JOIN usuarios u ON u.id = n.id_usuario
           WHERE n.id_usuario = %s
           ORDER BY n.id DESC""",
        (id_usuario,),
    )
    result = rows_to_list(cur) if result is None else []
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/notificacoes", methods=["POST"])
def criar_notificacao():
    body = request.get_json(silent=True) or {}
    for campo in ["id_usuario", "descricao"]:
        if not body.get(campo):
            return json_error(f"Campo obrigatório ausente: {campo}")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO notificacoes (id_usuario, descricao) VALUES (%s, %s)",
            (body["id_usuario"], body["descricao"]),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao enviar notificação: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Notificação enviada com sucesso."})


@app.route("/notificacoes/<int:nid>", methods=["DELETE"])
def deletar_notificacao(nid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM notificacoes WHERE id = %s", (nid,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Notificação não encontrada.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao remover notificação: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Notificação removida com sucesso."})
