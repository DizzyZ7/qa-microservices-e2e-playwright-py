import pytest


@pytest.mark.api
def test_health(api_client):
    assert api_client.health() == {"status": "ok"}


@pytest.mark.api
def test_live(api_client):
    assert api_client.live() == {"status": "ok"}


@pytest.mark.api
def test_ready(api_client):
    assert api_client.ready() == {
        "status": "ok",
        "checks": {"app": "ok", "database": "ok"},
    }


@pytest.mark.api
def test_health_response_contains_request_id(api_client):
    response = api_client.health_raw()

    assert response.status == 200
    assert response.headers["x-request-id"]


@pytest.mark.api
def test_health_response_contains_security_headers(api_client):
    response = api_client.health_raw(headers={"X-Request-ID": "health-sec-check"})

    assert response.status == 200
    assert response.headers["x-request-id"] == "health-sec-check"
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "no-referrer"
    assert response.headers["cache-control"] == "no-store"
