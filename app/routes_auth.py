import logging

from fastapi import APIRouter, HTTPException, Request

from app.models import LoginRequest, Role, Token
from app.rate_limit import rate_limit_login
from app.security import USERS, create_access_token, verify_password

logger = logging.getLogger("api")

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(body: LoginRequest, request: Request) -> Token:
    rate_limit_login(request)
    user = USERS.get(body.username)
    if not user or not verify_password(body.password, user.hashed_password):
        logger.info("login_failed username=%s", body.username)
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    logger.info("login_ok username=%s role=%s", user.username, user.role.value)
    access_token = create_access_token(username=user.username, role=user.role)
    return Token(access_token=access_token)

