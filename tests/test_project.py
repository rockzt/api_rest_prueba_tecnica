import json

def test_api_status(client):
    response = client.get("/healthycheck")
    assert b'Project Working Correctly!!!' in response.data

def test_api_get_orders(client):
    response = client.get("orders/order")
    raw = response.data
    d = json.loads(raw.decode('unicode_escape'))
    print(d)
    assert True