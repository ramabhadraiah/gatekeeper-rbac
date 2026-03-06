from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.config import ACCESS_TOKEN_MINUTES, JWT_ALG, JWT_SECRET
from app.models import Role, User, UserInDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# in-memory users
USERS: dict[str, UserInDB] = {
    "admin": UserInDB(username="admin", role=Role.admin, hashed_password=pwd_context.hash("admin123"))
}


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(*, username: str, role: Role) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    payload = {"sub": username, "role": role.value, "exp": exp}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    unauth = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        username = payload.get("sub")
        role = payload.get("role")
        if not username or not role:
            raise unauth
    except JWTError:
        raise unauth

    user = USERS.get(username)
    if not user:
        raise unauth
    return User(username=user.username, role=user.role)


def require_roles(*roles: Role):
    allowed = {r.value for r in roles}

    async def dep(user: User = Depends(get_current_user)) -> User:
        if user.role.value not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user

    return dep

