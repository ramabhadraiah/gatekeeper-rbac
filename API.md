RBAC Demo API — HTTP API Documentation
=====================================

Base URL
--------

- Local/Docker: `http://localhost:8000`

Authentication
--------------

This API uses Bearer tokens (JWT).

- Add this header to authenticated requests:

```
Authorization: Bearer <access_token>
```

Roles
-----

Valid roles:

- `admin`
- `manager`
- `operator`
- `viewer`

Permissions:

- **Public**
  - `GET /health`
  - `POST /auth/login`
- **Admin**
  - `POST /users`
- **Admin + Manager**
  - `GET /users`
- **Manager**
  - `POST /tasks/execute`
- **Any authenticated user**
  - `GET /tasks/{task_id}`

Common responses / errors
-------------------------

- **401 Unauthorized**: missing/invalid token
- **403 Forbidden**: authenticated but not enough permissions
- **429 Too Many Requests**: login rate limit hit
- **400 Bad Request**: invalid input (ex: pagination params)

Endpoints
---------

### Health

#### `GET /health` (public)

Response:

```json
{ "status": "ok" }
```

### Auth

#### `POST /auth/login` (public, rate-limited)

Request body:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

Notes:

- Rate limit is **per IP per minute** (config: `RATE_LIMIT_LOGIN`).

### Users

#### `POST /users` (admin only)

Request body:

```json
{
  "username": "manager1",
  "password": "manager123",
  "role": "manager"
}
```

Response (201):

```json
{
  "username": "manager1",
  "role": "manager"
}
```

#### `GET /users?page=1&size=20` (admin + manager)

Query params:

- `page`: integer, \(>= 1\) (default: 1)
- `size`: integer, \(1..100\) (default: 20)

Response:

```json
[
  { "username": "admin", "role": "admin" },
  { "username": "manager1", "role": "manager" }
]
```

Notes:

- This demo stores users **in memory** and sorts by username.

### Tasks

Tasks are executed in the background using **Celery + Redis**.

#### `POST /tasks/execute` (manager only)

Request body:

```json
{
  "payload": {
    "job_type": "report",
    "parameters": { "range": "last_7_days" }
  }
}
```

Response (202):

```json
{
  "id": "<task-id>",
  "status": "PENDING",
  "result": null,
  "error": null
}
```

#### `GET /tasks/{task_id}` (any authenticated user)

Response (example, still running):

```json
{
  "id": "<task-id>",
  "status": "RUNNING",
  "result": null,
  "error": null
}
```

Response (example, completed):

```json
{
  "id": "<task-id>",
  "status": "COMPLETED",
  "result": {
    "echo": { "job_type": "report" },
    "processed_at": "2026-03-06T12:00:00+00:00"
  },
  "error": null
}
```

Task status values:

- `PENDING`
- `RUNNING`
- `COMPLETED`
- `FAILED`

Configuration
-------------

Environment variables:

- `JWT_SECRET` (default: `dev-secret`)
- `ACCESS_TOKEN_MINUTES` (default: `60`)
- `REDIS_URL` (default in Docker: `redis://redis:6379/0`)
- `RATE_LIMIT_LOGIN` (default: `10` per minute per IP)
- `LOG_LEVEL` (default: `INFO`)

