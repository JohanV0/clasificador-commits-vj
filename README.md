# Clasificador de Commits

Sistema de clasificación de commits con modelo de lenguaje local (Ollama) + API FastAPI + PostgreSQL, todo en Docker.

## Arquitectura

Cliente -> FastAPI (puerto 8000) -> PostgreSQL (puerto 5432)
                              -> Ollama gemma3:270m (puerto 11434)

- API: FastAPI + Python 3.12
- Base de datos: PostgreSQL 15 con rol app_ia de privilegios minimos
- Modelo: gemma3:270m servido por Ollama en el host
- CI: GitHub Actions (lint + tests)

## Requisitos

- Ubuntu 22.04 o superior
- Docker + Docker Compose
- Ollama instalado con el modelo gemma3:270m
- Python 3.12 (para desarrollo local)

## Instalacion rapida

git clone git@github.com:JohanV0/clasificador-commits-vj.git
cd clasificador-commits-vj
cp .env.example .env
docker compose up -d --build
docker compose ps

La API queda disponible en http://localhost:8000/docs

## Endpoints

- GET /  -> Healthcheck
- GET /commits -> Lista los ultimos 50 commits
- POST /commits -> Crea un commit nuevo

Ejemplo:

curl -X POST http://localhost:8000/commits -H "Content-Type: application/json" -d '{"mensaje": "feat: nuevo endpoint", "categoria": "feature"}'

## Pruebas

pytest tests/ -v
k6 run tests/k6/load_test.js
python scripts/caracterizar_modelo.py

## Respaldo de la base de datos

docker exec clasificador_db pg_dump -U admin -d clasificador_db > backups/backup_$(date +%Y%m%d).sql

## Estructura del proyecto

- app/            Codigo de la API FastAPI
- backups/        Respaldos de PostgreSQL (no versionados)
- db/             Scripts de inicializacion de la BD
- docs/           Informe tecnico y manual
- scripts/        Scripts auxiliares (caracterizacion)
- tests/          Pruebas unitarias y de carga
- .github/workflows/  CI
- docker-compose.yml
- Dockerfile
- requirements.txt

## Autor

Johan V. — SENA, Complementaria
