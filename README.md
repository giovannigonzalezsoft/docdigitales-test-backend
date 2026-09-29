# DocDigitales Test Backend

API desarrollada con FastAPI, PostgreSQL, SQLAlchemy Async, Alembic y UV.

## Requisitos

- Python 3.12+
- PostgreSQL
- UV

## Configuración

### 1. Instalar dependencias

```bash
uv sync
```

### 2. Configurar variables de entorno

El proyecto incluye un archivo `.env.example`.

Crear el archivo `.env`:

```bash
cp .env.example .env
```

Configurar las variables de acuerdo con tu entorno:

```env
APP_NAME=DocDigitales Test
APP_ENV=development
API_PREFIX=/api/v1

DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres
DATABASE_DB=docdigitales-test

PAC_SHOULD_FAIL=false
```

`PAC_SHOULD_FAIL` permite simular un error del PAC para probar el flujo de timbrado fallido.

## Base de datos

Crear previamente la base de datos configurada en `DATABASE_DB`.

Las migraciones de Alembic se ejecutan automáticamente al iniciar la aplicación.

Opcionalmente se puede ejecutar el archivo de seed incluido en el proyecto para cargar datos de prueba.

## Ejecutar la API

```bash
uv run uvicorn app.main:app --reload
```

Swagger estará disponible en:

```text
http://localhost:8000/docs
```

## Ejecutar tests

```bash
uv run pytest -v
```

Para ejecutar únicamente los tests de timbrado:

```bash
uv run pytest tests/test_timbrado_routes.py -v
```

## Migraciones

Las migraciones se aplican automáticamente al iniciar la API.

## Pregunta de diseño

**Si el job que timbra una factura se ejecuta dos veces por accidente (por ejemplo, un reinicio del worker a mitad del proceso), ¿cómo evitarías que la factura se timbre dos veces?**

Verificaría si la factura ya tiene un estado de procesado o timbrado y si cuenta con un UUID fiscal por si el proceso se ejecuta de nuevo validaría estos criterios antes de intentar timbrarla otra vez.

Además, si la factura se timbró correctamente y por alguna razon el PAC falla y la respuesta no llegó a la API, utilizaría una clave de idempotencia para evitar generar un segundo timbre. Si el timbrado ya existe recupero el UUID fiscal y actualizo el estado de la factura y en caso de que no entonces la intento timbrar.