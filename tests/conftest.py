import os
import re
import time
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from playwright.sync_api import Page, Playwright, APIRequestContext

from core.api_client import ApiClient
from core.db import create_db_engine, delete_order
from core.settings import settings


def _safe_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", name)


def _wait_for_base_url(timeout_seconds: float = 5.0) -> None:
    deadline = time.time() + timeout_seconds
    health_url = f"{settings.base_url}/health"

    while time.time() < deadline:
        try:
            with urlopen(health_url, timeout=1.0) as response:
                if response.status == 200:
                    return
        except URLError:
            time.sleep(0.25)

    pytest.skip(
        f"Service is not reachable at {settings.base_url}. "
        "Start the stack before running E2E tests."
    )


@pytest.fixture(scope="session", autouse=True)
def _env_defaults():
    os.environ.setdefault("BASE_URL", settings.base_url)
    os.environ.setdefault("DATABASE_URL", settings.database_url)
    os.environ.setdefault("APP_USERNAME", settings.app_username)
    os.environ.setdefault("APP_PASSWORD", settings.app_password)


@pytest.fixture(scope="session")
def db_engine():
    return create_db_engine()


@pytest.fixture(autouse=True)
def ensure_service_ready(request):
    if request.node.get_closest_marker("api") or request.node.get_closest_marker("ui"):
        _wait_for_base_url()


@pytest.fixture
def cleanup_orders(db_engine):
    created: list[int] = []
    yield created
    for order_id in created:
        delete_order(db_engine, order_id)


@pytest.fixture
def api_request_context(playwright: Playwright) -> APIRequestContext:
    context = playwright.request.new_context(base_url=settings.base_url)
    yield context
    context.dispose()


@pytest.fixture
def api_client(api_request_context: APIRequestContext) -> ApiClient:
    return ApiClient(api_request_context)


@pytest.fixture
def authed_page(page: Page):
    # Быстрая авторизация через browser context API вместо UI-формы.
    r = page.context.request.post(
        f"{settings.base_url}/api/auth/login",
        form={"username": settings.app_username, "password": settings.app_password},
    )
    assert r.ok, f"Login failed with status {r.status}: {r.text()}"
    return page


@pytest.fixture(autouse=True)
def trace_on_failure(request):
    if request.node.get_closest_marker("ui") is None:
        yield
        return

    context = request.getfixturevalue("context")
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield
    failed = getattr(request.node, "rep_call", None) and request.node.rep_call.failed
    if failed:
        os.makedirs("artifacts/traces", exist_ok=True)
        trace_path = f"artifacts/traces/{_safe_name(request.node.nodeid)}.zip"
        context.tracing.stop(path=trace_path)
    else:
        context.tracing.stop()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
