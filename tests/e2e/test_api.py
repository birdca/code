import uuid

import requests

import config


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(id: int):
    return f"batcher-{id}-{random_suffix()}"


def random_orderid():
    return f"order-{random_suffix()}"


def test_get_root():
    r = requests.get(config.get_api_url())

    assert r.status_code == 200


def test_api_returns_allocation(add_stock):
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock(
        [
            (laterbatch, sku, 100, "2011-01-02"),
            (earlybatch, sku, 100, "2011-01-01"),
            (otherbatch, othersku, 100),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 200
    assert r.json()["batchref"] == earlybatch


def test_allocations_are_persisted(add_stock):
    sku, othersku = random_sku(), random_sku("other")
    earlybatch = random_batchref(1)
    laterbatch = random_batchref(2)
    otherbatch = random_batchref(3)
    add_stock(
        [
            (laterbatch, sku, 100, "2011-01-02"),
            (earlybatch, sku, 100, "2011-01-01"),
            (otherbatch, othersku, 100),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku, "qty": 100}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 200
    assert r.json()["batchref"] == earlybatch

    data = {"orderid": random_orderid(), "sku": sku, "qty": 100}
    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 200
    assert r.json()["batchref"] == laterbatch


def test_400_message_for_out_of_stock(add_stock):
    sku = random_sku()
    otherbatch = random_batchref(1)
    add_stock(
        [
            (otherbatch, sku, 0),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku, "qty": 100}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 400
    assert r.json()["detail"] == f"Out of stock for sku {sku}"


def test_400_message_for_invalid_sku(add_stock):
    sku1 = random_sku()
    sku2 = random_sku()
    otherbatch = random_batchref(1)
    add_stock(
        [
            (otherbatch, sku1, 100),
        ]
    )
    data = {"orderid": random_orderid(), "sku": sku2, "qty": 100}
    url = config.get_api_url()
    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 400
    assert r.json()["detail"] == f"Invalid sku {sku2}"
