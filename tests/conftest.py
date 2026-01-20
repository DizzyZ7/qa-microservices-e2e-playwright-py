import os
import re
import pytest
from playwright.sync_api import Page, APIRequestContext

from core.api_client import ApiClient
from core.db import create_db_engine, delete_order
from core.settings import settings

def _safe_name(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", name)

@pytest.fixture(scope="session", autouse=True)
def _env_defaults():
    settings.base_url = os.getenv("BASE_URL", settings.base_url)
    settings.database_url = os.getenv("DATABASE_URL", settings.database_url)
    settings.app_username = os.getenv("APP_USERNAME", settings.app_username)
    settings.app_password = os.getenv("APP_PASSWORD", settings.app_password)

@pytest.fixture(scope="session")
def db_engine():
    return create_db_engine()

@pytest.fixture
def cleanup_orders(db_engine):
    created: list[int] = []
    yield created
    for order_id in created:
        delete_order(db_engine, order_id)

@pytest.fixture
def api_client(request: APIRequestContext) -> ApiClient:
    return ApiClient(request)

@pytest.fixture
def authed_page(page: Page):
    r = page.request.post(
        f"{settings.base_url}/api/auth/login",
        data={"username": settings.app_username, "password": settings.app_password},
    )
    r.raise_for_status()
    return page

@pytest.fixture(autouse=True)
def trace_on_failure(context, request):
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
