from fastapi import FastAPI
from pydantic import BaseModel
import os
import psycopg2

app = FastAPI(title="Clasificador de Commits")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin_pass@db:5432/clasificador_db")

class Commit(BaseModel):
    mensaje: str
    categoria: str = None

def get_db():
    return psycopg2.connect(DATABASE_URL)

@app.get("/")
def root():
    return {"status": "ok", "servicio": "clasificador-commits"}

@app.get("/commits")
def listar_commits():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, mensaje, categoria FROM commits ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "mensaje": r[1], "categoria": r[2]} for r in rows]

@app.post("/commits")
def crear_commit(commit: Commit):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO commits (mensaje, categoria) VALUES (%s, %s) RETURNING id",
        (commit.mensaje, commit.categoria)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "mensaje": commit.mensaje, "categoria": commit.categoria}
