from datetime import date, timedelta

from model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_qty():
    batch = Batch("batch A", "Furniture A", 10, today)
    order_line = OrderLine("order A", "Furniture A", 1)
    batch.allocate(order_line)

    assert batch.qty == 9


def test_can_allocate_if_available_greater_than_required():
    batch = Batch("batch A", "Furniture A", 10, today)
    order_line = OrderLine("order A", "Furniture A", 1)

    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_available_smaller_than_required():
    batch = Batch("batch A", "Furniture A", 0, today)
    order_line = OrderLine("order A", "Furniture A", 1)

    assert batch.can_allocate(order_line) == False


def test_can_allocate_if_available_equal_to_required():
    batch = Batch("batch A", "Furniture A", 1, today)
    order_line = OrderLine("order A", "Furniture A", 1)

    assert batch.can_allocate(order_line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch A", "Furniture A", 1, today)
    order_line = OrderLine("order A", "Furniture B", 1)

    assert batch.can_allocate(order_line) == False


def test_allocation_is_idempotent():
    batch = Batch("batch A", "Furniture A", 1, today)
    order_line = OrderLine("order A", "Furniture A", 1)
    batch.allocate(order_line)
    batch.allocate(order_line)

    assert batch.qty == 0


def test_deallocate():
    batch = Batch("batch A", "Furniture A", 1, today)
    order_line = OrderLine("order A", "Furniture A", 1)
    batch.allocate(order_line)
    batch.deallocate(order_line)

    assert batch.qty == 1


def test_can_only_deallocate_allocated_lines():
    batch = Batch("batch A", "Furniture A", 1, today)
    order_line = OrderLine("order A", "Furniture B", 1)
    # batch.allocate(order_line)
    batch.deallocate(order_line)

    assert batch.qty == 1
