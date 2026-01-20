from playwright.sync_api import Page, expect
from core.settings import settings

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.username = page.locator("#username")
        self.password = page.locator("#password")
        self.submit = page.locator("#submit")
        self.error = page.locator("#error")

    def open(self):
        self.page.goto(f"{settings.base_url}/login")

    def login(self, username: str, password: str):
        self.username.fill(username)
        self.password.fill(password)
        self.submit.click()

    def expect_login_failed(self):
        expect(self.error).to_be_visible()
