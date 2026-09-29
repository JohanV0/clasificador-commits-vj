-- Creamos un rol con privilegios mínimos para la aplicación
CREATE ROLE app_ia WITH LOGIN PASSWORD 'app_ia_pass';

-- Le damos permiso de conexión a la base de datos
GRANT CONNECT ON DATABASE clasificador_db TO app_ia;

-- Le damos permiso de uso sobre el esquema public
GRANT USAGE ON SCHEMA public TO app_ia;

-- Creamos la tabla PRIMERO
CREATE TABLE IF NOT EXISTS commits (
    id SERIAL PRIMARY KEY,
    mensaje TEXT NOT NULL,
    categoria TEXT,
    creado_en TIMESTAMP DEFAULT NOW()
);

-- Ahora sí, damos permisos sobre la tabla existente
GRANT SELECT, INSERT, UPDATE ON commits TO app_ia;

-- Permiso para usar la secuencia del id
GRANT USAGE, SELECT ON SEQUENCE commits_id_seq TO app_ia;
