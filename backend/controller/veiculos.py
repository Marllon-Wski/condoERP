

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
#  VEÍCULOS
# ─────────────────────────────────────────────────────────

@app.route("/veiculos", methods=["GET"])
def listar_veiculos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT v.*, u.nome AS nome_usuario
           FROM veiculos v
           LEFT JOIN usuarios u ON u.id = v.id_usuario
           ORDER BY v.placa"""
    )
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/veiculos/<int:vid>", methods=["GET"])
def buscar_veiculo(vid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """SELECT v.*, u.nome AS nome_usuario
           FROM veiculos v
           LEFT JOIN usuarios u ON u.id = v.id_usuario
           WHERE v.id = %s""",
        (vid,),
    )
    row = cur.fetchone()
    response = row_to_dict(cur, row) if row else None
    cur.close()
    conn.close()
    if not row:
        return json_error("Veículo não encontrado.", 404)
    return json_ok(response)


@app.route("/veiculos/usuario/<int:id_usuario>", methods=["GET"])
def veiculos_por_usuario(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM veiculos WHERE id_usuario = %s ORDER BY placa",
        (id_usuario,),
    )
    result = rows_to_list(cur)
    cur.close()
    conn.close()
    return json_ok(result)


@app.route("/veiculos", methods=["POST"])
def criar_veiculo():
    body = request.get_json(silent=True) or {}
    for campo in ["placa", "id_usuario"]:
        if not body.get(campo):
            return json_error(f"Campo obrigatório ausente: {campo}")

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO veiculos (id_usuario, placa, descricao, documento)
               VALUES (%s, %s, %s, %s)""",
            (
                body.get("id_usuario"),
                body.get("placa").upper(),
                body.get("descricao"),
                body.get("documento"),
            ),
        )
        conn.commit()
        novo_id = cur.lastrowid
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao cadastrar veículo: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_created({"id": novo_id, "mensagem": "Veículo cadastrado com sucesso."})


@app.route("/veiculos/<int:vid>", methods=["PUT"])
def atualizar_veiculo(vid):
    body = request.get_json(silent=True) or {}
    campos = ["placa", "descricao", "documento"]
    updates = {k: body[k] for k in campos if k in body}
    if not updates:
        return json_error("Nenhum campo válido para atualizar.")

    if "placa" in updates:
        updates["placa"] = updates["placa"].upper()

    set_clause = ", ".join(f"{k} = %s" for k in updates)
    valores = list(updates.values()) + [vid]

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            f"UPDATE veiculos SET {set_clause} WHERE id = %s", valores
        )
        if cur.rowcount == 0:
            return json_error("Veículo não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(f"Erro ao atualizar: {e.msg}", 409)
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Veículo atualizado com sucesso."})


@app.route("/veiculos/<int:vid>", methods=["DELETE"])
def deletar_veiculo(vid):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM veiculos WHERE id = %s", (vid,))
        conn.commit()
        if cur.rowcount == 0:
            return json_error("Veículo não encontrado.", 404)
    except Error as e:
        conn.rollback()
        return json_error(
            "Não é possível excluir: veículo possui registros vinculados.", 409
        )
    finally:
        cur.close()
        conn.close()

    return json_ok({"mensagem": "Veículo removido com sucesso."})
