import psycopg2
from db.db_utils import establish_connection
from db.config import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT

migration_file_path = "./migration.sql"
conn = establish_connection()
cur = conn.cursor()

try:
    with open(migration_file_path, "r") as migration_file:
        migration_sql = migration_file.read()
        cur.execute(migration_sql)

    conn.commit()
    conn.close()

    print("Migrations Succeeded")

except psycopg2.Error as e:
    print("Error executing migration:", e)

finally:
    if conn is not None:
        conn.close()
