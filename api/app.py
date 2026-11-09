import os
from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def conexion():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )

def consulta(sql, params=()):
    conn = conexion()
    cur = conn.cursor()
    cur.execute(sql, params)
    filas = cur.fetchall()
    conn.close()
    return [{"tienda": t, "ticket_promedio": float(p)} for t, p in filas]

@app.route("/")
def inicio():
    return {"estado": "ok"}

@app.route("/resultados")
def todos():
    return jsonify(consulta("SELECT tienda, ticket_promedio FROM resultados ORDER BY tienda"))

@app.route("/resultados/<tienda>")
def una(tienda):
    filas = consulta("SELECT tienda, ticket_promedio FROM resultados WHERE tienda = %s", (tienda,))
    if not filas:
        return {"error": "no encontrada"}, 404
    return jsonify(filas[0])

@app.route("/resultados", methods=["POST"])
def crear():
    d = request.get_json()
    conn = conexion()
    cur = conn.cursor()
    cur.execute("INSERT INTO resultados VALUES (%s, %s)", (d["tienda"], d["ticket_promedio"]))
    conn.commit()
    conn.close()
    return d, 201

@app.route("/resultados/<tienda>", methods=["DELETE"])
def borrar(tienda):
    conn = conexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM resultados WHERE tienda = %s", (tienda,))
    conn.commit()
    conn.close()
    return {"borrada": tienda}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
