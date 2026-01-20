import pytest

@pytest.mark.api
def test_health(api_client):
    api_client.health()
