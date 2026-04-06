import os

from fastapi import APIRouter, Depends, Form, HTTPException, Response
from sqlalchemy.orm import Session

from . import crud
from .dependencies import get_db
from .errors import OrderNotFoundError
from .schemas import OrderCreate, OrderOut


APP_USERNAME = os.getenv("APP_USERNAME", "demo")
APP_PASSWORD = os.getenv("APP_PASSWORD", "demo")

router = APIRouter(prefix="/api", tags=["api"])


@router.post("/orders", response_model=OrderOut)
def api_create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, payload.item)


@router.get("/orders", response_model=list[OrderOut])
def api_list_orders(db: Session = Depends(get_db)):
    return crud.list_orders(db)


@router.get("/orders/{order_id}", response_model=OrderOut)
def api_get_order(order_id: int, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise OrderNotFoundError(order_id)
    return order


@router.post("/orders/{order_id}/process", response_model=OrderOut)
def api_process_order(order_id: int, db: Session = Depends(get_db)):
    return crud.mark_order_processed(db, order_id)


@router.post("/auth/login")
def api_login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    if username != APP_USERNAME or password != APP_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    response.set_cookie("session", "ok", httponly=True, samesite="lax")
    return {"ok": True}
