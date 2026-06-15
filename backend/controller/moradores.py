

from flask import Flask, jsonify, request, abort
from mysql.connector import Error
from dotenv import load_dotenv

from condoERP.backend.config import app, logger
from condoERP.backend.utils.helpers import (
    get_connection,
    row_to_dict,
    rows_to_list,
    json_ok,
    json_created,
    json_error
)

# ─────────────────────────────────────────────────────────
#  MORADORES
# ─────────────────────────────────────────────────────────


@app.route("/moradores", methods=["GET"])
def listar_moradores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT m.*, u.nome, u.cpf, u.telefone,
                  a.numero AS apto_numero, a.descricao AS apto_descricao
           FROM moradores m
           JOIN usuarios u ON u.id = m.id_user
           LEFT JOIN apartamentos a ON a.id = m.id_apto
           ORDER BY u.nome"""
    )
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/moradores/<int:id_usuario>", methods=["GET"])
def buscar_morador(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT m.*, u.nome, u.cpf, u.telefone, 
                  a.numero AS apto_numero, a.descricao AS apto_descricao
           FROM moradores m
           JOIN usuarios u ON u.id = m.id_user
           LEFT JOIN apartamentos a ON a.id = m.id_apto
           WHERE m.id_user = %s""",
        (id_usuario,),
    )
    row = cur.fetchone()
    response = row_to_dict(cur, row) if row else None
    cur.close()
    conn.close()
    if not row:
        return json_error("Morador não encontrado.", 404)
    return json_ok(response)


@app.route("/moradores", methods=["POST"])
def criar_morador():
    body = request.get_json(silent=True) or {}
    for campo in ["id_user", "id_apto"]:
        if campo not in body:
            return json_error(f"Campo obrigatório ausente: {campo}", 400)
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO moradores (id_user, id_veiculo, id_vaga, id_apto)
               VALUES (%s, %s, %s, %s)""",
            (
                body.get("id_user"),
                body.get("id_veiculo"),
                body.get("id_vaga"),
                body.get("id_apto"),
            ),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao criar morador: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Morador vinculado com sucesso."})


@app.route("/moradores/<int:id_usuario>", methods=["PUT"])
def atualizar_morador(id_usuario):
    body = request.get_json(silent=True) or {}
    campos = ["id_veiculo", "id_vaga", "id_apto"]
    updates = {k: body[k] for k in campos if k in body}
    if not updates:
        return json_error("Nenhum campo válido para atualizar.")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    valores = list(updates.values()) + [id_usuario]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE moradores SET {set_clause} WHERE id_user = %s", valores
        )
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Morador não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Morador atualizado com sucesso."})


@app.route("/moradores/<int:id_usuario>", methods=["DELETE"])
def deletar_morador(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM moradores WHERE id_user = %s", (id_usuario,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Morador não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(
            "Não é possível excluir: morador possui registros vinculados.", 409
        )
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Morador removido com sucesso."})
