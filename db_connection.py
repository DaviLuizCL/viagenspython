import psycopg2
from psycopg2 import sql
import sys
# Dados de conexão
dbname = "db_teste"
user = "usr_teste"
password = "9126"
host = "localhost"
port = "5432"  # Porta padrão do PostgreSQL

# Tentar conectar ao banco de dados
try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Conexão bem-sucedida!")

except psycopg2.Error as e:
    print(f"Erro ao conectar ao PostgreSQL: {e}")
    sys.exit(1)

# Criar um cursor para realizar operações no banco de dados
cur = conn.cursor()

# Exemplo de criação de tabela
create_table_query = '''
CREATE TABLE IF NOT EXISTS exemplo (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    idade INT
)
'''

try:
    cur.execute(create_table_query)
    conn.commit()  # Confirmar a criação da tabela
    print("Tabela criada com sucesso!")
except psycopg2.Error as e:
    print(f"Erro ao criar tabela: {e}")
    conn.rollback()

# Exemplo de inserção de dados
insert_query = '''
INSERT INTO exemplo (nome, idade) VALUES (%s, %s)
'''

try:
    cur.execute(insert_query, ("Alice", 30))
    cur.execute(insert_query, ("Bob", 25))
    conn.commit()  # Confirmar a inserção dos dados
    print("Dados inseridos com sucesso!")
except psycopg2.Error as e:
    print(f"Erro ao inserir dados: {e}")
    conn.rollback()

# Exemplo de consulta de dados
select_query = '''
SELECT * FROM exemplo
'''

try:
    cur.execute(select_query)
    rows = cur.fetchall()
    for row in rows:
        print(f"id: {row[0]}, nome: {row[1]}, idade: {row[2]}")
except psycopg2.Error as e:
    print(f"Erro ao consultar dados: {e}")

# Fechar o cursor e a conexão
cur.close()
conn.close()
