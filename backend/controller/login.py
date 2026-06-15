
from flask import Flask, jsonify, request, abort
from mysql.connector import Error
from dotenv import load_dotenv

from condoERP.backend.config import app, logger
from condoERP.backend.controller import usuarios
from condoERP.backend.utils.helpers import (
    encriptar_senha,
    get_connection,
    row_to_dict,
    rows_to_list,
    json_ok,
    json_created,
    json_error
)

# ──────────────────────────────────────────────────────────────
# LOGINS
# ──────────────────────────────────────────────────────────────


@app.route("/login", methods=["GET"])
def listar_logins():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM login ORDER BY ilogin")
        logins = rows_to_list(cur)
    except Error as e:
        return json_error(f"Erro ao listar logins: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()
    return json_ok(logins)


@app.route("/login/<int:lid>", methods=["GET"])
def buscar_login(lid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM login WHERE id = %s", (lid,))
        row = cur.fetchone()
        if not row:
            return json_error("Login não encontrado.", 404)
        # build the dict while the cursor is still open
        response = row_to_dict(cur, row)
    except Error as e:
        return json_error(f"Erro ao buscar login: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok(response)


@app.route("/login", methods=["POST"])
def criar_login():
    body = request.get_json() or {}
    for campo in ["nome", "ilogin", "telefone", "cpf", "data_nasc", "senha"]:
        if campo not in body:
            return json_error(f"Campo obrigatório ausente: {campo}", 400)

    senha_encriptada = encriptar_senha(body["senha"])
    tipo_acesso = body.get("tipo_acesso", "morador")
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO usuarios (nome, idade, cpf, telefone, data_nasc)"
            " VALUES (%s, %s, %s, %s, %s)",
            (
                body.get("nome"),
                body.get("idade"),
                body.get("cpf"),
                body.get("telefone"),
                body.get("data_nasc"),
            ),
        )
        user_id = cur.lastrowid
        cur.execute(
            "INSERT INTO login (id_user, ilogin, senha, tipo_acesso) VALUES (%s, %s, %s, %s)",
            (user_id, body.get("ilogin"), senha_encriptada, body.get("tipo_acesso")),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao criar login: {e.msg}", 409)
    finally:
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Login criado com sucesso."})


@app.route("/login/<int:lid>", methods=["PUT"])
def atualizar_login(lid):
    body = request.get_json(silent=True) or {}
    campos = ["nome", "senha"]
    updates = {k: body[k] for k in campos if k in body}
    if not updates:
        return json_error("Nenhum campo válido para atualizar.")

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    valores = list(updates.values()) + [lid]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE login SET {set_clause} WHERE id = %s", valores
        )
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Login não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Login atualizado com sucesso."})


@app.route("/login/<int:lid>", methods=["DELETE"])
def deletar_login(lid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM login WHERE id = %s", (lid,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Login não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(
            "Não é possível excluir: login possui registros vinculados.", 409
        )
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Login removido com sucesso."})


@app.route("/login/auth", methods=["POST"])
def login_usuario():
    body = request.get_json(silent=True) or {}
    ilogin = body.get("ilogin")
    senha = body.get("senha")
    if not ilogin or not senha:
        return json_error("Login e senha são obrigatórios.", 400)

    senha_encriptada = encriptar_senha(senha)
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT l.senha, l.id_user, l.tipo_acesso FROM login as l WHERE ilogin = %s",
            (ilogin,)
        )
        row = cur.fetchone()
        if not row:
            return json_error("Credenciais inválidas.", 401)

        senha_armazenada, id_user, tipo_acesso = row
        if senha_armazenada != senha_encriptada:
            return json_error("Credenciais inválidas.", 401)

        return json_ok({"id_user": id_user, "tipo_acesso": tipo_acesso})
    except Error as e:
        logger.error(f"Erro ao autenticar: {e.msg}")
        return json_error(f"Erro ao autenticar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()
