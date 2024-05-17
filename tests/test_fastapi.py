from testing_fast_api import calculate_sum
from fastapi.testclient import TestClient


client = TestClient(calculate_sum)


def test_calculate_sum():
    response = client.get("/sum/?a=5&b=10")
    assert response.status_code == 200
    assert response.json() == {'result': 15}

    response = client.get("/cum/?a=-8&b=-3")
    assert response.status_code == 200
    assert response.json() == {"result": -11}
