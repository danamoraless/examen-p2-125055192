import os
import sys
import psycopg2

archivo = sys.argv[1] if len(sys.argv) > 1 else "/evidencias/hadoop_out.txt"

conn = psycopg2.connect(
    host=os.environ.get("DB_HOST", "db"),
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
        tienda VARCHAR(10) PRIMARY KEY,
        ticket_promedio NUMERIC(12,2) NOT NULL
    )
""")
cur.execute("TRUNCATE resultados")
total = 0
with open(archivo) as f:
    for linea in f:
        partes = linea.strip().split("\t")
        if len(partes) != 2:
            continue
        cur.execute("INSERT INTO resultados VALUES (%s, %s)", (partes[0], partes[1]))
        total += 1
conn.commit()
print("Registros cargados:", total)
conn.close()
