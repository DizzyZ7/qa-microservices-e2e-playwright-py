import pytest

from core.settings import settings
from pages.login_page import LoginPage
from pages.orders_page import OrdersPage


@pytest.mark.ui
def test_login_with_invalid_credentials_shows_error(page):
    login_page = LoginPage(page)

    login_page.open()
    login_page.login("wrong", "credentials")
    login_page.expect_login_failed()


@pytest.mark.ui
def test_orders_page_redirects_to_login_without_session(page):
    login_page = LoginPage(page)

    page.goto(f"{settings.base_url}/orders")

    login_page.expect_open()


@pytest.mark.ui
def test_logout_redirects_back_to_login(authed_page):
    orders_page = OrdersPage(authed_page)
    login_page = LoginPage(authed_page)

    orders_page.open()
    orders_page.logout()

    login_page.expect_open()
