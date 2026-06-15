

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
#  VISITANTES
# ─────────────────────────────────────────────────────────

@app.route("/visitantes", methods=["GET"])
def listar_visitantes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT v.*, u.nome, u.cpf, u.telefone,
                  um.nome AS nome_morador
           FROM visitantes v
           JOIN usuarios u ON u.id = v.id_user
           LEFT JOIN moradores m ON m.id = v.id_morador
           LEFT JOIN usuarios um ON um.id = m.id_user
           ORDER BY u.nome"""
    )
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/visitantes/<int:vid>", methods=["GET"])
def buscar_visitante(vid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT v.*, u.nome, u.cpf, u.telefone,
                  um.nome AS nome_morador
           FROM visitantes v
           JOIN usuarios u ON u.id = v.id_user
           LEFT JOIN moradores m ON m.id = v.id_morador
           LEFT JOIN usuarios um ON um.id = m.id_user
           WHERE v.id = %s""",
        (vid,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return json_error("Visitante não encontrado.", 404)
    return json_ok(row_to_dict(cur, row))


@app.route("/visitantes", methods=["POST"])
def criar_visitante():
    body = request.get_json(silent=True) or {}
    if not body.get("id_user"):
        return json_error("Campo obrigatório ausente: id_user")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO visitantes (id_user, id_veiculo, id_vaga, id_morador)
               VALUES (%s, %s, %s, %s)""",
            (
                body["id_user"],
                body.get("id_veiculo"),
                body.get("id_vaga"),
                body.get("id_morador"),
            ),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao registrar visitante: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Visitante registrado com sucesso."})


@app.route("/visitantes/<int:vid>", methods=["PUT"])
def atualizar_visitante(vid):
    body = request.get_json(silent=True) or {}
    campos = ["id_veiculo", "id_vaga", "id_morador"]
    updates = {k: body[k] for k in campos if k in body}
    if not updates:
        return json_error("Nenhum campo válido para atualizar.")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    valores = list(updates.values()) + [vid]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE visitantes SET {set_clause} WHERE id = %s", valores
        )
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Visitante não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Visitante atualizado com sucesso."})


@app.route("/visitantes/<int:vid>", methods=["DELETE"])
def deletar_visitante(vid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM visitantes WHERE id = %s", (vid,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Visitante não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao remover visitante: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Visitante removido com sucesso."})

