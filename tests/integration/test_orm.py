from datetime import date

from sqlalchemy import text

from domain.model import Batch, OrderLine


def test_orderline_mapper_can_load_lines(session):
    session.execute(
        text(
            "INSERT INTO order_lines (orderid, sku, qty) VALUES "
            '("order1", "RED-CHAIR", 12),'
            '("order1", "RED-TABLE", 13),'
            '("order2", "BLUE-LIPSTICK", 14)'
        )
    )
    expected = [
        OrderLine("order1", "RED-CHAIR", 12),
        OrderLine("order1", "RED-TABLE", 13),
        OrderLine("order2", "BLUE-LIPSTICK", 14),
    ]

    assert session.query(OrderLine).all() == expected


def test_orderline_mapper_can_save_lines(session):
    order_line = OrderLine("order1", "RED-CHAIR", 12)
    session.add(order_line)
    session.commit()

    rows = list(session.execute(text("SELECT orderid, sku, qty FROM order_lines")))

    assert rows == [("order1", "RED-CHAIR", 12)]


def test_retrieving_batches(session):
    session.execute(
        text(
            "INSERT INTO batches (ref, sku, qty, eta) VALUES "
            '("batch1", "RED-CHAIR", 12, null),'
            '("batch2", "RED-TABLE", 13, "2011-04-11")'
        )
    )
    expected = [
        Batch("batch1", "RED-CHAIR", 12),
        Batch("batch2", "RED-TABLE", 13, date(2011, 4, 11)),
    ]

    assert session.query(Batch).all() == expected


def test_saving_batches(session):
    batch = Batch("batch1", "RED-CHAIR", 12)
    session.add(batch)
    session.commit()

    rows = session.execute(text("SELECT ref, sku, qty, eta FROM batches"))

    assert list(rows) == [("batch1", "RED-CHAIR", 12, None)]


def test_saving_allocations(session):
    batch = Batch("batch1", "RED-CHAIR", 12)
    line = OrderLine("order1", "RED-CHAIR", 12)
    batch.allocate(line)
    session.add(batch)
    session.commit()

    rows = list(session.execute(text("SELECT orderline_id, batch_id FROM allocations")))

    assert rows == [(line.id, batch.ref)]


def test_retrieving_allocations(session):
    session.execute(
        text(
            'INSERT INTO order_lines (orderid, sku, qty) VALUES ("order1", "sku1", 12)'
        )
    )
    [[orderline_id]] = session.execute(
        text("SELECT id FROM order_lines WHERE orderid=:orderid AND sku=:sku"),
        dict(orderid="order1", sku="sku1"),
    )
    session.execute(
        text(
            'INSERT INTO batches (ref, sku, qty, eta) VALUES ("batch1", "sku1", 12, null)'
        )
    )
    [[batch_ref]] = session.execute(
        text("SELECT ref FROM batches WHERE ref=:ref"), dict(ref="batch1")
    )
    session.execute(
        text("INSERT INTO allocations (orderline_id, batch_id) VALUES (:oid, :bid)"),
        dict(oid=orderline_id, bid=batch_ref),
    )

    batch = session.query(Batch).one()

    assert batch._allocations == {OrderLine("order1", "sku1", 12)}
