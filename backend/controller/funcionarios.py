
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
#  FUNCIONÁRIOS
# ─────────────────────────────────────────────────────────

@app.route("/funcionarios", methods=["GET"])
def listar_funcionarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT f.*, u.nome, u.cpf, u.telefone
           FROM funcionarios f
           JOIN usuarios u ON u.id = f.id_user
           ORDER BY u.nome"""
    )
    response = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(response)


@app.route("/funcionarios/<int:id_usuario>", methods=["GET"])
def buscar_funcionario(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT f.*, u.nome, u.cpf, u.telefone
               FROM funcionarios f
               JOIN usuarios u ON u.id = f.id_user
               WHERE f.id_user = %s""",
            (id_usuario,),
        )
        row = cur.fetchone()
        if not row:
            return json_error("Funcionário não encontrado.", 404)
        response = row_to_dict(cur, row) if row else None
    finally:
        cur.close()
        conn.close()

    return json_ok(response)


@app.route("/funcionarios", methods=["POST"])
def criar_funcionario():
    body = request.get_json(silent=True) or {}
    for campo in ["id_user", "descricao"]:
        if campo not in body:
            return json_error(f"Campo obrigatório ausente: {campo}", 400)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO funcionarios (id_user, id_veiculo, id_vaga, descricao)
               VALUES (%s, %s, %s, %s)""",
            (
                body.get("id_user"),
                body.get("id_veiculo"),
                body.get("id_vaga"),
                body.get("descricao"),
            ),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao cadastrar funcionário: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Funcionário cadastrado com sucesso."})


@app.route("/funcionarios/<int:id_usuario>", methods=["PUT"])
def atualizar_funcionario(id_usuario):
    body = request.get_json(silent=True) or {}
    campos = ["id_veiculo", "id_vaga", "descricao"]
    updates = {k: body[k] for k in campos if k in body}
    if not updates:
        return json_error("Nenhum campo válido para atualizar.")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    valores = list(updates.values()) + [id_usuario]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE funcionarios SET {set_clause} WHERE id_user = %s", valores
        )
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Funcionário não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Funcionário atualizado com sucesso."})


@app.route("/funcionarios/<int:id_usuario>", methods=["DELETE"])
def deletar_funcionario(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM funcionarios WHERE id_user = %s",
                    (id_usuario,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Funcionário não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(
            "Não é possível excluir: funcionário possui registros vinculados.", 409
        )
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Funcionário removido com sucesso."})
