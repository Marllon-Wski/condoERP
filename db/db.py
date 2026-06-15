#!/usr/bin/env python3
"""
Script para criar o banco MySQL a partir do arquivo `db.sql`.

Uso:
  python db.py --host localhost --user root --password secret
"""
import os
import re
import argparse
import mysql.connector


def read_sql_statements(path: str):
	with open(path, 'r', encoding='utf-8') as f:
		sql = f.read()
	# remover comentários de linha começando com --
	sql = re.sub(r'--.*?\n', '\n', sql)
	# dividir por ponto-e-vírgula
	parts = [s.strip() for s in sql.split(';') if s.strip()]
	return parts


def execute_statements(conn, statements):
	cursor = conn.cursor()
	for stmt in statements:
		try:
			cursor.execute(stmt)
		except Exception as err:
			print(f"Aviso: erro ao executar statement: {err}")
	conn.commit()
	cursor.close()


def create_from_sql_file(host: str, user: str, password: str, port: int, sql_path: str):
	cfg = dict(host=host, user=user, password=password, port=port)
	conn = mysql.connector.connect(**cfg)
	try:
		stmts = read_sql_statements(sql_path)
		# Desabilita checagem de foreign keys para evitar problemas de ordem
		execute_statements(conn, ['SET FOREIGN_KEY_CHECKS=0'])
		execute_statements(conn, stmts)
		execute_statements(conn, ['SET FOREIGN_KEY_CHECKS=1'])
		print('Script SQL executado com sucesso.')
	finally:
		conn.close()


def main():
	parser = argparse.ArgumentParser(description='Criar banco MySQL a partir de db.sql')
	parser.add_argument('--host', default='localhost')
	parser.add_argument('--user', default='root')
	parser.add_argument('--password', default='')
	parser.add_argument('--port', type=int, default=3306)
	parser.add_argument('--sql', default=os.path.join(os.path.dirname(__file__), 'db.sql'))
	args = parser.parse_args()

	if not os.path.exists(args.sql):
		raise SystemExit(f"Arquivo SQL não encontrado: {args.sql}")

	try:
		create_from_sql_file(args.host, args.user, args.password, args.port, args.sql)
	except mysql.connector.Error as e:
		print(f"Erro de conexão/execução: {e}")
		raise


if __name__ == '__main__':
	main()

