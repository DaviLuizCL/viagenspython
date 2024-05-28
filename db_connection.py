import psycopg2
from psycopg2 import sql
import sys
# Dados de conexão
dbname = "db_teste"
user = "postgres"
password = ""
host = "localhost"
port = "5432"  # Porta padrão do PostgreSQL

# Tentar conectar ao banco de dados
def create_connection():
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return conn 

    except Exception as e:
        print("erro ao conectar no banco de dados")
        print(e)
        return None



def insert_user(nome, email, senha):
    conn = create_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query="INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        cursor.execute(query, (nome, email, senha))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print("Erro ao inserir dados")
        print(e)
        return False

def insert_travel(destino, inicio, termino, numero_de_pessoas, roteiro):
    conn = create_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        query="INSERT INTO viagens (destino, inicio, termino, numero_de_pessoas, roteiro) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (destino, inicio, termino, numero_de_pessoas, roteiro))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print("Erro ao inserir dados")
        print(e)
        return False

