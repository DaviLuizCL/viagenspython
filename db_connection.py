import mariadb
import sys

try:
    conn = mariadb.connect(
            user="root",
            password="9126",
            host="127.0.0.1",
            port="3306",
            database="teste_projeto"
            )


except mariadb.Error as e:
    print(f"Error connecting to MariaDB platform: {e}")
    sys.exit(1)


cur = conn.cursor()
