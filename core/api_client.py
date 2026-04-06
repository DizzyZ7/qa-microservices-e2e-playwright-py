from playwright.sync_api import APIRequestContext
from playwright.sync_api._generated import APIResponse


def _assert_ok(response: APIResponse) -> APIResponse:
    if not response.ok:
        raise AssertionError(
            f"Request failed with status {response.status}: {response.text()}"
        )
    return response


class ApiClient:
    def __init__(self, request: APIRequestContext):
        self.request = request

    def create_order(self, item: str) -> dict:
        return _assert_ok(self.request.post("/api/orders", data={"item": item})).json()

    def get_order(self, order_id: int) -> dict:
        return _assert_ok(self.request.get(f"/api/orders/{order_id}")).json()

    def list_orders(self) -> list[dict]:
        return _assert_ok(self.request.get("/api/orders")).json()

    def process_order(self, order_id: int) -> None:
        _assert_ok(self.request.post(f"/api/orders/{order_id}/process"))

    def login(self, username: str, password: str):
        return self.request.post(
            "/api/auth/login",
            form={"username": username, "password": password},
        )

    def create_order_raw(self, payload: dict, headers: dict | None = None):
        return self.request.post("/api/orders", data=payload, headers=headers)

    def get_order_raw(self, order_id: int, headers: dict | None = None):
        return self.request.get(f"/api/orders/{order_id}", headers=headers)

    def process_order_raw(self, order_id: int, headers: dict | None = None):
        return self.request.post(f"/api/orders/{order_id}/process", headers=headers)

    def health_raw(self, headers: dict | None = None):
        return self.request.get("/health", headers=headers)

    def health(self) -> dict:
        return _assert_ok(self.request.get("/health")).json()

    def live(self) -> dict:
        return _assert_ok(self.request.get("/health/live")).json()

    def ready(self) -> dict:
        return _assert_ok(self.request.get("/health/ready")).json()
