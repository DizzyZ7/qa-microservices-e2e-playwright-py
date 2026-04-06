import pytest

from core.db import get_order_status, order_exists


@pytest.mark.api
def test_create_order_persists_in_database(api_client, db_engine, cleanup_orders):
    order = api_client.create_order(item="Laptop")
    cleanup_orders.append(order["id"])

    assert order["item"] == "Laptop"
    assert order["status"] == "NEW"
    assert get_order_status(db_engine, order["id"]) == "NEW"


@pytest.mark.api
def test_process_order_updates_status(api_client, db_engine, cleanup_orders):
    order = api_client.create_order(item="Keyboard")
    cleanup_orders.append(order["id"])

    api_client.process_order(order["id"])

    processed_order = api_client.get_order(order["id"])
    assert processed_order["status"] == "PROCESSED"
    assert get_order_status(db_engine, order["id"]) == "PROCESSED"


@pytest.mark.api
def test_list_orders_contains_created_order(api_client, cleanup_orders):
    order = api_client.create_order(item="Mouse")
    cleanup_orders.append(order["id"])

    orders = api_client.list_orders()

    assert any(item["id"] == order["id"] and item["item"] == "Mouse" for item in orders)


@pytest.mark.api
def test_login_rejects_invalid_credentials(api_client):
    response = api_client.login("wrong", "credentials")

    assert response.status == 401
    body = response.json()
    assert body["error"]["code"] == "invalid_credentials"
    assert body["error"]["message"] == "Invalid credentials"
    assert body["error"]["request_id"]


@pytest.mark.api
def test_cleanup_fixture_tracks_created_order(api_client, db_engine, cleanup_orders):
    order = api_client.create_order(item="Temporary item")
    cleanup_orders.append(order["id"])

    assert order_exists(db_engine, order["id"]) is True


@pytest.mark.api
def test_get_order_returns_structured_404(api_client):
    response = api_client.get_order_raw(999999)

    assert response.status == 404
    body = response.json()
    assert body["error"]["code"] == "order_not_found"
    assert body["error"]["message"] == "Order 999999 was not found"
    assert body["error"]["request_id"]


@pytest.mark.api
def test_process_order_returns_structured_404(api_client):
    response = api_client.process_order_raw(999999)

    assert response.status == 404
    body = response.json()
    assert body["error"]["code"] == "order_not_found"
    assert body["error"]["message"] == "Order 999999 was not found"
    assert body["error"]["request_id"]


@pytest.mark.api
def test_create_order_rejects_blank_item(api_client):
    response = api_client.create_order_raw({"item": "   "})

    assert response.status == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Request validation failed"
    assert body["error"]["details"] == [
        {
            "field": "item",
            "message": "Value error, Item must not be blank",
        }
    ]
    assert body["error"]["request_id"]


@pytest.mark.api
def test_create_order_rejects_too_short_item(api_client):
    response = api_client.create_order_raw({"item": "PC"})

    assert response.status == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Request validation failed"
    assert body["error"]["details"] == [
        {
            "field": "item",
            "message": "String should have at least 3 characters",
        }
    ]
    assert body["error"]["request_id"]


@pytest.mark.api
def test_api_error_preserves_request_id(api_client):
    response = api_client.get_order_raw(999999, headers={"X-Request-ID": "req-404-check"})

    assert response.status == 404
    assert response.headers["x-request-id"] == "req-404-check"
    assert response.json() == {
        "error": {
            "code": "order_not_found",
            "message": "Order 999999 was not found",
            "request_id": "req-404-check",
        }
    }
