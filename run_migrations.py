import psycopg2
from db import establish_connection

# migration_file_path = "./db/migrations/teardown.sql"
migration_file_path = "./db/migrations/migration.sql"

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
