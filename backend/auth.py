import hashlib
import hmac
import time

from fastapi import HTTPException, Request
from starlette.responses import Response

from .config import HR_ADMIN_PASSWORD, SESSION_COOKIE, SESSION_SECRET


def _signature(payload: str) -> str:
    return hmac.new(SESSION_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()


def set_session(response: Response, secure: bool) -> None:
    expires = str(int(time.time()) + 60 * 60 * 12)
    token = f"{expires}.{_signature(expires)}"
    response.set_cookie(
        SESSION_COOKIE,
        token,
        max_age=60 * 60 * 12,
        httponly=True,
        secure=secure,
        samesite="strict",
        path="/",
    )


def clear_session(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE, path="/", httponly=True, samesite="strict")


def require_admin(request: Request) -> None:
    if not HR_ADMIN_PASSWORD or not SESSION_SECRET:
        raise HTTPException(status_code=503, detail="Set HR_ADMIN_PASSWORD in the .env file.")
    token = request.cookies.get(SESSION_COOKIE, "")
    try:
        expires, signature = token.split(".", 1)
        valid = int(expires) > int(time.time()) and hmac.compare_digest(signature, _signature(expires))
    except (ValueError, TypeError):
        valid = False
    if not valid:
        raise HTTPException(status_code=401, detail="Please sign in to access the HR portal.")
