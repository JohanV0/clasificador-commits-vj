import os
import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "postgresql://admin:admin_pass@localhost:5432/clasificador_db")

from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_listar_commits():
    r = client.get("/commits")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_crear_commit():
    payload = {"mensaje": "test: commit desde pytest", "categoria": "test"}
    r = client.post("/commits", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["mensaje"] == payload["mensaje"]
    assert data["categoria"] == payload["categoria"]

def test_app_ia_no_puede_borrar():
    """Prueba de seguridad: el rol app_ia no puede borrar commits."""
    import psycopg2
    conn = psycopg2.connect(
        "postgresql://app_ia:app_ia_pass@localhost:5432/clasificador_db"
    )
    conn.autocommit = True
    cur = conn.cursor()
    with pytest.raises(psycopg2.errors.InsufficientPrivilege):
        cur.execute("DELETE FROM commits")
    cur.close()
    conn.close()
