from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timezone

from fastapi import HTTPException, Request

from app.config import RATE_LIMIT_LOGIN

_login_hits: dict[str, deque[float]] = defaultdict(deque)


def rate_limit_login(request: Request) -> None:
    ip = request.client.host if request.client else "unknown"
    now = datetime.now(timezone.utc).timestamp()
    hits = _login_hits[ip]
    while hits and (now - hits[0]) > 60:
        hits.popleft()
    if len(hits) >= RATE_LIMIT_LOGIN:
        raise HTTPException(status_code=429, detail="Too many login attempts, slow down")
    hits.append(now)

