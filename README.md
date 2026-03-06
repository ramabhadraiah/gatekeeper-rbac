RBAC Demo API
=============

Small FastAPI backend demo with:

- JWT login
- role-based access control (admin/manager/operator/viewer)
- users stored in memory (just for demo)
- background jobs via Celery + Redis
- simple rate limiting on login (in-memory)
- basic logging
- simple pagination for `GET /users`

## Quickstart (Docker)

This starts:
- `api` on port 8000
- `redis`
- `worker` (Celery)

```bash
docker compose up --build
```

Open Swagger: `http://localhost:8000/docs`

## Quickstart (local)

You need Python + Redis running somewhere.

```bash
pip install -r requirements.txt
set JWT_SECRET=dev-secret
set REDIS_URL=redis://localhost:6379/0
uvicorn app.main:app --reload
```

In a second terminal (worker):

```bash
set REDIS_URL=redis://localhost:6379/0
celery -A app.celery_app:celery_app worker --loglevel=INFO
```

## Default user

- username: `admin`
- password: `admin123`
- role: `admin`

## Endpoints

- `GET /health` (public)
- `POST /auth/login` (public, rate-limited)
- `POST /users` (admin only)
- `GET /users?page=1&size=20` (admin + manager)
- `POST /tasks/execute` (manager only)
- `GET /tasks/{task_id}` (any authenticated user)

## API documentation

Written API docs live in `API.md`.

Interactive docs are also available via FastAPI's built-in OpenAPI:

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Example requests (curl)

Login:

```bash
curl -X POST http://localhost:8000/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```

## Config

- `JWT_SECRET` (default: `dev-secret`)
- `ACCESS_TOKEN_MINUTES` (default: `60`)
- `REDIS_URL` (default in Docker: `redis://redis:6379/0`)
- `RATE_LIMIT_LOGIN` (default: `10` per minute per IP)
- `LOG_LEVEL` (default: `INFO`)

