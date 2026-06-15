
import logging
import hashlib
from flask import Flask, jsonify, request, abort
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from datetime import date, datetime
from decimal import Decimal

from condoERP.backend.config import DB_CONFIG, logger


# ── Helpers ───────────────────────────────────────────────


def get_connection():
    # Abre e retorna uma conexão com o banco.
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        logger.error("Erro de conexão: %s", e)
        abort(503, description="Não foi possível conectar ao banco de dados.")


def serialize(obj):
    # Serializa tipos especiais para JSON.
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    return obj


def row_to_dict(cursor, row):
    # Converte uma linha de resultado em dicionário.
    return {
        col[0]: serialize(val)
        for col, val in zip(cursor.description, row)
    }


def rows_to_list(cursor):
    # Converte todas as linhas em lista de dicionários.
    return [row_to_dict(cursor, row) for row in cursor.fetchall()]


def json_ok(data, status=200):
    return jsonify({"sucesso": True,  "dados": data}), status


def json_created(data):
    return jsonify({"sucesso": True,  "dados": data}), 201


def json_error(msg, status=400):
    return jsonify({"sucesso": False, "erro": msg}), status


def encriptar_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def comparar_senhas(senha_fornecida, senha_armazenada):
    return encriptar_senha(senha_fornecida) == senha_armazenada

def validar_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Validação do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    
    # Validação do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10
    
    return digito1 == int(cpf[9]) and digito2 == int(cpf[10])