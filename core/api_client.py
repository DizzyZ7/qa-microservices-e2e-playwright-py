from playwright.sync_api import APIRequestContext
from .settings import settings


class ApiClient:
    def __init__(self, request: APIRequestContext):
        self.request = request

    def create_order(self, item: str) -> int:
        # Сервер ожидает JSON (OrderCreate)
        r = self.request.post(
            f"{settings.base_url}/api/orders",
            json={"item": item},
        )
        r.raise_for_status()
        return r.json()["id"]

    def process_order(self, order_id: int) -> None:
        r = self.request.post(f"{settings.base_url}/api/orders/{order_id}/process")
        r.raise_for_status()

    def health(self) -> None:
        r = self.request.get(f"{settings.base_url}/health")
        r.raise_for_status()
