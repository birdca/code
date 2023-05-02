from datetime import date, timedelta
import pytest

from model import Batch, OrderLine, OutOfStock, allocation

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_prefers_warehouse_batches_to_shipments():
    in_stock_batch = Batch('batch A', 'Furniture A', 1, today)
    shipment_batch = Batch('batch A', 'Furniture A', 1, tomorrow)
    order_line = OrderLine('order A', 'Furniture A', 1)
    allocation(order_line, [shipment_batch, in_stock_batch])

    assert in_stock_batch.qty == 0
    assert shipment_batch.qty == 1


def test_prefers_earlier_batches():
    earliest_batch = Batch('batch A', 'Furniture A', 1, today)
    medium_batch = Batch('batch A', 'Furniture A', 1, tomorrow)
    later_batch = Batch('batch A', 'Furniture A', 1, later)
    order_line = OrderLine('order A', 'Furniture A', 1)
    allocation(order_line, [medium_batch, earliest_batch, later_batch])

    assert earliest_batch.qty == 0
    assert medium_batch.qty == 1
    assert later_batch.qty == 1


def test_returns_allocted_batch_ref():
    in_stock_batch = Batch('batch A', 'Furniture A', 1, today)
    shipment_batch = Batch('batch A', 'Furniture A', 1, tomorrow)
    order_line = OrderLine('order A', 'Furniture A', 1)
    get_al = allocation(order_line, [shipment_batch, in_stock_batch])

    assert get_al == in_stock_batch.ref


def test_raise_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch A', 'Furniture A', 0, today)
    order_line = OrderLine('order A', 'Furniture A', 1)

    with pytest.raises(OutOfStock, match='Furniture A'):
        allocation(order_line, [batch])
