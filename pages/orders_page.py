from playwright.sync_api import Page, expect
from core.settings import settings

class OrdersPage:
    def __init__(self, page: Page):
        self.page = page
        self.orders_list = page.locator("#orders")
        self.order_id = page.locator("#order_id")
        self.process_btn = page.locator("#process")

    def open(self):
        self.page.goto(f"{settings.base_url}/orders")

    def expect_order_visible(self, order_id: int):
        expect(self.page.locator(f"#order-{order_id}")).to_be_visible()

    def process_order(self, order_id: int):
        self.order_id.fill(str(order_id))
        self.process_btn.click()
