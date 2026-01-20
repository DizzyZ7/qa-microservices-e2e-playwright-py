import os
from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from .db import Base, engine, SessionLocal
from .schemas import OrderCreate, OrderOut
from . import crud

APP_USERNAME = os.getenv("APP_USERNAME", "demo")
APP_PASSWORD = os.getenv("APP_PASSWORD", "demo")

app = FastAPI(title="Demo Orders Service")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/orders", response_model=OrderOut)
def api_create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, payload.item)

@app.get("/api/orders", response_model=list[OrderOut])
def api_list_orders(db: Session = Depends(get_db)):
    return crud.list_orders(db)

@app.post("/api/orders/{order_id}/process", response_model=OrderOut)
def api_process_order(order_id: int, db: Session = Depends(get_db)):
    try:
        return crud.mark_order_processed(db, order_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Order not found")

@app.post("/api/auth/login")
def login(username: str, password: str, response: Response):
    if username != APP_USERNAME or password != APP_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    response.set_cookie("session", "ok", httponly=True)
    return {"ok": True}

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
      <body>
        <h1>Demo App</h1>
        <a href="/login">Login</a>
      </body>
    </html>
    """

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <html>
      <body>
        <h2>Login</h2>
        <form method="post" action="/ui/login">
          <label>Username</label><input name="username" id="username"/>
          <label>Password</label><input name="password" id="password" type="password"/>
          <button id="submit" type="submit">Sign in</button>
        </form>
      </body>
    </html>
    """

@app.post("/ui/login", response_class=HTMLResponse)
def ui_login(username: str = "", password: str = "", response: Response = None):
    if username != APP_USERNAME or password != APP_PASSWORD:
        return HTMLResponse("<p id='error'>Invalid</p><a href='/login'>Back</a>", status_code=401)
    response = HTMLResponse("<script>window.location='/orders'</script>")
    response.set_cookie("session", "ok", httponly=True)
    return response

def require_session(session: str | None):
    if session != "ok":
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/orders", response_class=HTMLResponse)
def orders_page(session: str | None = None, db: Session = Depends(get_db)):
    require_session(session)
    orders = crud.list_orders(db)
    items = "\n".join([f"<li id='order-{o.id}'>#{o.id} {o.item} [{o.status}]</li>" for o in orders])
    return f"""
    <html>
      <body>
        <h2>Orders</h2>
        <ul id="orders">{items}</ul>
        <form method="post" action="/ui/process">
          <label>Order ID</label>
          <input name="order_id" id="order_id"/>
          <button id="process" type="submit">Process</button>
        </form>
      </body>
    </html>
    """

@app.post("/ui/process", response_class=HTMLResponse)
def ui_process(order_id: int, session: str | None = None, db: Session = Depends(get_db)):
    require_session(session)
    try:
        crud.mark_order_processed(db, order_id)
    except ValueError:
        return HTMLResponse("<p id='notfound'>Not found</p><a href='/orders'>Back</a>", status_code=404)
    return HTMLResponse("<script>window.location='/orders'</script>")
