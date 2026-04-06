from dataclasses import dataclass


@dataclass
class AppError(Exception):
    code: str
    message: str
    status_code: int


class OrderNotFoundError(AppError):
    def __init__(self, order_id: int):
        super().__init__(
            code="order_not_found",
            message=f"Order {order_id} was not found",
            status_code=404,
        )
