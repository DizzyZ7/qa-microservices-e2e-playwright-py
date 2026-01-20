from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from .settings import settings

def create_db_engine() -> Engine:
    return create_engine(settings.database_url, pool_pre_ping=True)

def get_order_status(engine: Engine, order_id: int) -> str | None:
    with engine.connect() as conn:
        row = conn.execute(text("SELECT status FROM orders WHERE id=:id"), {"id": order_id}).fetchone()
        return row[0] if row else None

def delete_order(engine: Engine, order_id: int) -> None:
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM orders WHERE id=:id"), {"id": order_id})
