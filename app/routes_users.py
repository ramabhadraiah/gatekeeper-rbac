from fastapi import APIRouter, Depends, HTTPException

from app.models import Role, UserCreateRequest, UserInDB, UserResponse
from app.security import USERS, hash_password, require_roles

router = APIRouter()


@router.post(
    "",
    response_model=UserResponse,
    status_code=201,
    dependencies=[Depends(require_roles(Role.admin))],
)
async def create_user(body: UserCreateRequest) -> UserResponse:
    if body.username in USERS:
        raise HTTPException(status_code=400, detail="Username already exists")
    USERS[body.username] = UserInDB(
        username=body.username,
        role=body.role,
        hashed_password=hash_password(body.password),
    )
    return UserResponse(username=body.username, role=body.role)


@router.get(
    "",
    response_model=list[UserResponse],
    dependencies=[Depends(require_roles(Role.admin, Role.manager))],
)
async def list_users(page: int = 1, size: int = 20) -> list[UserResponse]:
    if page < 1 or size < 1 or size > 100:
        raise HTTPException(status_code=400, detail="Invalid pagination (page>=1, 1<=size<=100)")
    items = sorted(USERS.values(), key=lambda u: u.username)
    start = (page - 1) * size
    end = start + size
    return [UserResponse(username=u.username, role=u.role) for u in items[start:end]]

