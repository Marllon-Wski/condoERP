

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
#  OCORRÊNCIAS
# ─────────────────────────────────────────────────────────

@app.route("/ocorrencias", methods=["GET"])
def listar_ocorrencias():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT o.*, u.nome AS nome_usuario
           FROM ocorrencias o
           JOIN usuarios u ON u.id = o.id_usuario
           ORDER BY o.id DESC"""
    )
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/ocorrencias/<int:oid>", methods=["GET"])
def buscar_ocorrencia(oid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT o.*, u.nome AS nome_usuario
           FROM ocorrencias o
           JOIN usuarios u ON u.id = o.id_usuario
           WHERE o.id = %s""",
        (oid,),
    )
    row = cur.fetchone()
    result = row_to_dict(cur, row) if row else None
    cur.close()
    conn.close()
    if not row:
        return json_error("Ocorrência não encontrada.", 404)
    return json_ok(result)


@app.route("/ocorrencias/usuario/<int:id_usuario>", methods=["GET"])
def ocorrencias_por_usuario(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT o.*, u.nome AS nome_usuario
           FROM ocorrencias o
           JOIN usuarios u ON u.id = o.id_usuario
           WHERE o.id_usuario = %s
           ORDER BY o.id DESC""",
        (id_usuario,),
    )
    result = rows_to_list(cur) if result is not None else []
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/ocorrencias", methods=["POST"])
def criar_ocorrencia():
    body = request.get_json(silent=True) or {}
    for campo in ["id_usuario", "descricao"]:
        if not body.get(campo):
            return json_error(f"Campo obrigatório ausente: {campo}")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO ocorrencias (id_usuario, descricao) VALUES (%s, %s)",
            (body["id_usuario"], body["descricao"]),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao registrar ocorrência: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Ocorrência registrada com sucesso."})


@app.route("/ocorrencias/<int:oid>", methods=["PUT"])
def atualizar_ocorrencia(oid):
    body = request.get_json(silent=True) or {}
    if not body.get("descricao"):
        return json_error("Campo obrigatório ausente: descricao")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE ocorrencias SET descricao = %s WHERE id = %s",
            (body["descricao"], oid),
        )
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Ocorrência não encontrada.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Ocorrência atualizada com sucesso."})


@app.route("/ocorrencias/<int:oid>", methods=["DELETE"])
def deletar_ocorrencia(oid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM ocorrencias WHERE id = %s", (oid,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Ocorrência não encontrada.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao remover ocorrência: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Ocorrência removida com sucesso."})
