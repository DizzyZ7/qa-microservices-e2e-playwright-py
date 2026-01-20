import pytest
from core.db import get_order_status
from pages.orders_page import OrdersPage

@pytest.mark.ui
def test_order_lifecycle(api_client, page, authed_page, db_engine, cleanup_orders):
    order_id = api_client.create_order(item="Laptop")
    cleanup_orders.append(order_id)

    orders = OrdersPage(authed_page)
    orders.open()
    orders.expect_order_visible(order_id)

    orders.process_order(order_id)
    orders.expect_order_visible(order_id)

    status = get_order_status(db_engine, order_id)
    assert status == "PROCESSED"
