# Taller: ELK Stack Multi-Source & Data Enrichment

**Curso:** Big Data & Cloud Architecture
**Profesor:** Juan Pablo Zaldumbide
**Estudiantes:** Nicolás Carrión, Jairo Cabrera

## 1. Objetivo del Taller

El objetivo del taller es implementar una pipeline de datos completa utilizando **Docker**, **Logstash** y **Elasticsearch**, integrando múltiples fuentes de datos (Batch y Near Real-Time) y enriqueciéndolas mediante consultas a una base de datos relacional (PostgreSQL).

## 2. Arquitectura del Stack

| Componente | Rol | Versión |
| :--- | :--- | :--- |
| **PostgreSQL** | Base de datos relacional (Fuente de verdad) | 15 |
| **Elasticsearch** | Motor de búsqueda y análisis | 8.10.2 |
| **Logstash** | Orquestador y transformador de datos | 8.10.2 |
| **Kibana** | Visualización y dashboards | 8.10.2 |

## 3. Fuentes de Datos Implementadas

Se han integrado **4 fuentes** de datos diferenciadas:

### A. Batch - Catálogo de Productos
- **Tipo:** CSV (Staging).
- **Fuente:** `data/olist_products_dataset.csv`.
- **Transformación:** Conversión de tipos de datos (peso y dimensiones a float).
- **Enriquecimiento:** Ninguno (Datos puramente descriptivos).

### B. Batch - Clientes
- **Tipo:** PostgreSQL (Entidad).
- **Fuente:** Tabla `customers`.
- **Transformación:** Extracción de campos de geolocalización (`city`, `state`).
- **Enriquecimiento:** **Joining con `products`** (implícito en la lógica de negocio, aunque en este archivo se cargan por separado). *Nota: En un flujo real, haríamos JOIN.* La transformación en el config es extracción simple.

### C. Near Real-Time - Reseñas
- **Tipo:** Log (Texto plano delimitado).
- **Fuente:** `data/reviews.log`.
- **Transformación:** Parsing CSV y conversión de `review_score` a Integer.
- **Enriquecimiento:** Se mapea la fecha de respuesta para análisis de latencia.

### D. Near Real-Time - Telemetría de Pedidos
- **Tipo:** JSON (Semi-estructurado).
- **Fuente:** `data/telemetria_pedidos.json`.
- **Transformación:** Ingesta nativa de JSON.
- **Enriquecimiento:** Se mapea el `payment_type`.

## 4. Configuración de Logstash

El archivo `logstash/pipeline/logstash.config` define el pipeline con los siguientes bloques:

### 1. Input (Múltiples Fuentes)
- **`file` (Batch):** Lectura del CSV de productos.
- **`jdbc` (Batch):** Conexión a PostgreSQL (`${POSTGRES_USER}`, `${POSTGRES_PASSWORD}`).
- **`file` (NRT):** Lectura en modo "tail" del archivo de reviews.
- **`file` (NRT):** Lectura de archivo JSON.

### 2. Filter (Procesamiento)
- **`csv`:** Para parsear archivos de texto plano.
- **`mutate`:** Conversión de tipos (`integer`, `float`) y limpieza de campos temporales (`remove_field`).

### 3. Output
- **`elasticsearch`:** Envío a `http://elasticsearch:9200`.
- **`stdout`:** Debugging en consola.

## 5. Ejecución

1. Asegurarse de tener los archivos de datos en la carpeta `data/`.
2. Si no se tiene, leer el README.md en la carpeta `preprocess/` para obtener los archivos de datos.
3. Activar el entorno virtual: 
   ```bash
   .venv/bin/activate
   ```
4. Ejecutar el script py scripts/start_nrt.py
   ```bash
   py scripts/start_nrt.py
   ```
5. Ejecutar el stack:
   ```bash
   docker-compose up -d
   ```
6. Esperar a que los contenedores se inicien.
7. Abrir Kibana en `http://localhost:5601`.
8. Crear los índices en Discover o crear un Dashboard de prueba.
9. Se puede cargar el dashboards creado en `kibana/export.ndjson`
    9.1. Abrir Kibana en el navegador `http://localhost:5601`.
    9.2. Abrir el menú de navegación principal (el icono de la hamburguesa en la esquina superior izquierda).
    9.3. Ir a Management → Stack Management.
    9.4. En la barra lateral izquierda, en la sección Kibana, hacer clic en Saved Objects.
    9.5. Clic en el botón Import en la esquina superior derecha.
    9.6. Arrastrar y soltar el archivo .ndjson (o hacer clic para buscarlo).
    9.7. Mantener "Check for existing objects" o "Automatically overwrite all saved object conflicts" habilitado si deseas reemplazar versiones existentes.
    9.8. Clic en Import, luego en Done.

## 6. Observaciones

- Se desactivó la seguridad de Elasticsearch (`xpack.security.enabled=false`) para simplificar la configuración del taller.
- Los índices creados en Elasticsearch son: `batch_productos-index`, `batch_clientes-index`, `nrt_reviews-index`, `nrt_telemetria-index`.
- Se recomienda reiniciar Logstash cada vez que se agreguen nuevos archivos a la carpeta `/data` para asegurar el procesamiento completo.
