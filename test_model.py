from datetime import date, timedelta
import pytest

from model import Batch, OrderLine, OutOfStock, allocate

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch = Batch('batch A', 'Furniture A', 10, today)
    order_line = OrderLine('order A', 'Furniture A', 1)
    batch.allocate(order_line)

    assert batch.quantity == 9 


def test_can_allocate_if_available_greater_than_required():
    batch = Batch('batch A', 'Furniture A', 10, today)
    order_line = OrderLine('order A', 'Furniture A', 1)

    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_available_smaller_than_required():
    batch = Batch('batch A', 'Furniture A', 0, today)
    order_line = OrderLine('order A', 'Furniture A', 1)

    assert batch.can_allocate(order_line) == False


def test_can_allocate_if_available_equal_to_required():
    batch = Batch('batch A', 'Furniture A', 1, today)
    order_line = OrderLine('order A', 'Furniture A', 1)

    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch('batch A', 'Furniture A', 1, today)
    order_line = OrderLine('order A', 'Furniture B', 1)

    assert batch.can_allocate(order_line) == False


def test_can_only_deallocate_allocated_lines():
    batch = Batch('batch A', 'Furniture A', 1, today)
    order_line = OrderLine('order A', 'Furniture B', 1)
    batch.allocate(order_line)
    batch.deallocate(order_line)

    assert batch.quantity == 1


def test_allocation_is_idempotent():
    batch = Batch('batch A', 'Furniture A', 1, today)
    order_line = OrderLine('order A', 'Furniture A', 1)
    batch.allocate(order_line)
    batch.allocate(order_line)
    
    assert batch.quantity == 0


def test_prefers_warehouse_batches_to_shipments():
    in_stock_batch = Batch('batch A', 'Furniture A', 1, today)
    shipment_batch = Batch('batch A', 'Furniture A', 1, tomorrow)
    order_line = OrderLine('order A', 'Furniture A', 1)
    allocate(order_line, [shipment_batch, in_stock_batch])

    assert in_stock_batch.quantity == 0
    assert shipment_batch.quantity == 1


def test_prefers_earlier_batches():
    earliest_batch = Batch('batch A', 'Furniture A', 1, today)
    medium_batch = Batch('batch A', 'Furniture A', 1, tomorrow)
    later_batch = Batch('batch A', 'Furniture A', 1, later)
    order_line = OrderLine('order A', 'Furniture A', 1)
    allocate(order_line, [medium_batch, earliest_batch, later_batch])

    assert earliest_batch.quantity == 0
    assert medium_batch.quantity == 1
    assert later_batch.quantity == 1


def test_returns_allocted_batch_ref():
    in_stock_batch = Batch('batch A', 'Furniture A', 1, today)
    shipment_batch = Batch('batch A', 'Furniture A', 1, tomorrow)
    order_line = OrderLine('order A', 'Furniture A', 1)
    allocation = allocate(order_line, [shipment_batch, in_stock_batch])

    assert allocation == in_stock_batch.reference


def test_raise_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch A', 'Furniture A', 0, today)
    order_line = OrderLine('order A', 'Furniture A', 1)
    with pytest.raises(OutOfStock, match='Furniture A'):
        allocate(order_line, [batch])
