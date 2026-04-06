import os
from pathlib import Path

from fastapi import APIRouter, Cookie, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud
from .dependencies import get_db
from .errors import OrderNotFoundError


APP_USERNAME = os.getenv("APP_USERNAME", "demo")
APP_PASSWORD = os.getenv("APP_PASSWORD", "demo")
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

router = APIRouter(tags=["ui"])


def require_ui_session(session: str | None):
    if session != "ok":
        return RedirectResponse("/login", status_code=303)
    return None


@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/ui/login")
def ui_login(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
):
    if username != APP_USERNAME or password != APP_PASSWORD:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid"},
            status_code=401,
        )

    response = RedirectResponse("/orders", status_code=303)
    response.set_cookie("session", "ok", httponly=True, samesite="lax")
    return response


@router.get("/orders")
def orders_page(
    request: Request,
    session: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    redirect = require_ui_session(session)
    if redirect is not None:
        return redirect

    orders = crud.list_orders(db)
    return templates.TemplateResponse(
        "orders.html",
        {"request": request, "orders": orders, "error": None},
    )


@router.post("/ui/process")
def ui_process(
    request: Request,
    order_id: int = Form(...),
    session: str | None = Cookie(default=None),
    db: Session = Depends(get_db),
):
    redirect = require_ui_session(session)
    if redirect is not None:
        return redirect

    try:
        crud.mark_order_processed(db, order_id)
    except OrderNotFoundError:
        return templates.TemplateResponse(
            "orders.html",
            {"request": request, "orders": crud.list_orders(db), "error": "Not found"},
            status_code=404,
        )

    return RedirectResponse("/orders", status_code=303)


@router.post("/ui/logout")
def ui_logout():
    response = RedirectResponse("/login", status_code=303)
    response.delete_cookie("session")
    return response
