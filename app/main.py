import logging

from fastapi import FastAPI

from app.config import LOG_LEVEL
from app.routes_auth import router as auth_router
from app.routes_tasks import router as tasks_router
from app.routes_users import router as users_router

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger("api")

app = FastAPI(title="RBAC Demo API", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
