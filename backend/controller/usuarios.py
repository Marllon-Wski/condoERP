
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

# ──────────────────────────────────────────────────────────────
# USUÁRIOS
# ──────────────────────────────────────────────────────────────


@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM usuarios ORDER BY nome")
        usuarios = rows_to_list(cur)
    except Error as e:
        return json_error(f"Erro ao listar usuários: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()
    return json_ok(usuarios)


@app.route("/usuarios/<int:uid>", methods=["GET"])
def buscar_usuario(uid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (uid,))
        row = cur.fetchone()
        if not row:
            return json_error("Usuário não encontrado.", 404)
        # build the dict while the cursor is still open
        response = row_to_dict(cur, row)
    except Error as e:
        return json_error(f"Erro ao buscar usuário: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok(response)


@app.route("/usuarios", methods=["POST"])
def criar_usuario():
    body = request.get_json() or {}
    for campo in ["nome", "cpf"]:
        if campo not in body:
            return json_error(f"Campo obrigatório ausente: {campo}", 400)

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO usuarios (nome, idade, cpf, telefone)
               VALUES (%s, %s, %s, %s)""",
            (
                body.get("nome"),
                body.get("idade"),
                body.get("cpf"),
                body.get("telefone"),
            ),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao criar usuário: {e.msg}", 409)
    finally:
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Usuário criado com sucesso."})


@app.route("/usuarios/<int:uid>", methods=["PUT"])
def atualizar_usuario(uid):
    body = request.get_json(silent=True) or {}
    campos = ["nome", "idade", "telefone"]
    updates = {k: body[k] for k in campos if k in body}
    if not updates:
        return json_error("Nenhum campo válido para atualizar.")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    valores = list(updates.values()) + [uid]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE usuarios SET {set_clause} WHERE id = %s", valores
        )
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Usuário não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Usuário atualizado com sucesso."})


@app.route("/usuarios/<int:uid>", methods=["DELETE"])
def deletar_usuario(uid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM usuarios WHERE id = %s", (uid,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Usuário não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(
            "Não é possível excluir: usuário possui registros vinculados.", 409
        )
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Usuário removido com sucesso."})
