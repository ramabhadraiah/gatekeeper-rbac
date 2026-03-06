import logging

from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException

from app.celery_app import celery_app
from app.models import TaskCreateRequest, TaskResponse, TaskStatus, User
from app.security import get_current_user, require_roles, Role
from app.tasks import run_job

logger = logging.getLogger("api")

router = APIRouter()


@router.post(
    "/execute",
    response_model=TaskResponse,
    status_code=202,
    dependencies=[Depends(require_roles(Role.manager))],
)
async def execute_task(body: TaskCreateRequest) -> TaskResponse:
    async_result = run_job.delay(body.payload)
    logger.info("task_submitted id=%s", async_result.id)
    return TaskResponse(id=async_result.id, status=TaskStatus.pending)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str, _: User = Depends(get_current_user)) -> TaskResponse:
    result = AsyncResult(id=task_id, app=celery_app)
    if not result or not result.id:
        raise HTTPException(status_code=404, detail="Task not found")

    state = result.state
    if state in {"PENDING", "RECEIVED"}:
        status_value = TaskStatus.pending
    elif state in {"STARTED", "RETRY"}:
        status_value = TaskStatus.running
    elif state == "SUCCESS":
        status_value = TaskStatus.completed
    else:
        status_value = TaskStatus.failed

    task_result = result.result if status_value == TaskStatus.completed else None
    error = str(result.result) if status_value == TaskStatus.failed and result.result else None
    return TaskResponse(id=result.id, status=status_value, result=task_result, error=error)

