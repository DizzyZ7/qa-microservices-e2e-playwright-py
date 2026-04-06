from fastapi import APIRouter, HTTPException, Request

from .db import check_db_connection


router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/health/live")
def live():
    return {"status": "ok"}


@router.get("/health/ready")
def ready(request: Request):
    is_ready = getattr(request.app.state, "is_ready", False)
    db_ok = check_db_connection()

    if not is_ready or not db_ok:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "degraded",
                "checks": {
                    "app": "ok" if is_ready else "starting",
                    "database": "ok" if db_ok else "down",
                },
            },
        )

    return {"status": "ok", "checks": {"app": "ok", "database": "ok"}}
