from playwright.sync_api import Page, expect
from core.settings import settings


class OrdersPage:
    def __init__(self, page: Page):
        self.page = page
        self.orders_list = page.locator("#orders")
        self.order_id = page.locator("#order_id")
        self.process_btn = page.locator("#process")
        self.logout_btn = page.locator("#logout")

    def open(self):
        self.page.goto(f"{settings.base_url}/orders")
        expect(self.orders_list).to_be_visible()

    def expect_order_visible(self, order_id: int):
        expect(self.page.locator(f"#order-{order_id}")).to_be_visible()

    def expect_order_status(self, order_id: int, status: str):
        expect(self.page.locator(f"#order-{order_id}")).to_contain_text(f"[{status}]")

    def process_order(self, order_id: int):
        self.order_id.fill(str(order_id))
        self.process_btn.click()

    def logout(self):
        self.logout_btn.click()
