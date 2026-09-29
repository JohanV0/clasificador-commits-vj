# Informe técnico

## Ficha de caracterización del modelo

| Dato | Cómo obtenerlo | Valor |
|------|----------------|-------|
| Perfil de hardware | Sección 2 de la guía | C |
| RAM total del equipo | free -h | 5,6 GiB |
| Modelo y etiqueta | ollama list | gemma3:270m |
| Tamaño en disco | ollama list | 291 MB |
| Latencia de 5 ejecuciones (ms) | time curl ... cinco veces | 1437, 1419, 1471, 1462, 1454 |
| Latencia promedio | Promedio de las cinco | 1448,6 ms |
| RAM usada durante la inferencia | free -h mientras responde | 4,1 GiB |
| Calidad percibida (1 a 5) | Su criterio, con una frase que lo justifique | 2 - Confunde comandos de terminal con texto y alucina explicaciones, pero responde en español |

## Pruebas de carga y cuello de botella

### Resultados

- **k6 (40s, hasta 10 VUs)**: 220 requests, 0% de error, p95 = 18.18 ms.
- **Modelo gemma3:270m**: latencia promedio 1646 ms, mínimo 1459 ms, máximo 2095 ms.

### Análisis

El cuello de botella del sistema está en la **inferencia del modelo de lenguaje**, no en la API ni en la base de datos:

1. La API con FastAPI + PostgreSQL responde en ~16 ms promedio, con un p95 de 18 ms bajo 10 usuarios concurrentes.
2. En cambio, el modelo gemma3:270m tarda ~1.6 segundos por respuesta, **100 veces más**.
3. El modelo corre en CPU (AMD-V, sin GPU dedicada), con 5.6 GiB de RAM total, lo que limita el paralelismo.
4. OLLAMA_MAX_LOADED_MODELS=1 y OLLAMA_NUM_PARALLEL=1 (configurados en la Semana 1) fuerzan procesamiento en serie, lo cual es correcto para el perfil C pero impide atender varias clasificaciones a la vez.

### Conclusión

Para producción habría que:
- Escalar el modelo a uno más grande y con GPU.
- O bien, separar el servicio de inferencia en un servidor dedicado.
- La API y la base de datos ya están dimensionadas de sobra para el tráfico actual.

## Escalamiento

El sistema actual está dimensionado para el perfil C (5,6 GiB de RAM, sin GPU dedicada). Para llevarlo a producción:

### Corto plazo
- **Escalar el modelo**: reemplazar gemma3:270m por un modelo más grande (p. ej. llama3.2:3b o qwen2.5:7b) en un servidor con GPU.
- **Cache de resultados**: guardar clasificaciones ya hechas en PostgreSQL y consultar primero la caché antes de llamar al modelo.
- **Cola de tareas**: usar Redis + Celery para procesar clasificaciones en lote sin bloquear la API.

### Mediano plazo
- **Separar el servicio de inferencia** en su propio servidor con GPU (o usar un proveedor cloud: Together, Groq, etc.).
- **Réplicas de la API**: correr varias instancias de FastAPI detrás de un balanceador (nginx o Traefik).
- **PostgreSQL con réplica de lectura** si el volumen de commits crece mucho.

### Largo plazo
- **Kubernetes** para orquestar API + workers + modelos, con autoescalado horizontal.
- **Observabilidad**: Prometheus + Grafana para métricas, y Loki para logs.
- **Fine-tuning del modelo** con los commits ya clasificados de la empresa.

### Cuello de botella identificado

El límite actual es la **inferencia del modelo en CPU** (~1,6 s por respuesta). La API y PostgreSQL responden en ~16 ms, así que cualquier mejora en la arquitectura pasa por acelerar o paralelizar la inferencia.
