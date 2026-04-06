from sqlalchemy.orm import Session
from .errors import OrderNotFoundError
from .models import Order


def create_order(db: Session, item: str) -> Order:
    order = Order(item=item, status="NEW")
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def list_orders(db: Session) -> list[Order]:
    return db.query(Order).order_by(Order.id.desc()).all()


def get_order(db: Session, order_id: int) -> Order | None:
    return db.get(Order, order_id)


def mark_order_processed(db: Session, order_id: int) -> Order:
    order = get_order(db, order_id)
    if not order:
        raise OrderNotFoundError(order_id)
    order.status = "PROCESSED"
    db.commit()
    db.refresh(order)
    return order
