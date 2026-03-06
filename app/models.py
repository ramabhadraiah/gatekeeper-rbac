from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Role(str, Enum):
    admin = "admin"
    manager = "manager"
    operator = "operator"
    viewer = "viewer"


class User(BaseModel):
    username: str
    role: Role


class UserInDB(User):
    hashed_password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    role: Role


class UserResponse(BaseModel):
    username: str
    role: Role


class TaskStatus(str, Enum):
    pending = "PENDING"
    running = "RUNNING"
    completed = "COMPLETED"
    failed = "FAILED"


class TaskCreateRequest(BaseModel):
    payload: dict[str, Any] = Field(default_factory=dict)


class TaskResponse(BaseModel):
    id: str
    status: TaskStatus
    result: Any | None = None
    error: str | None = None


class TaskResult(BaseModel):
    echo: dict[str, Any]
    processed_at: datetime

