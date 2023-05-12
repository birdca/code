from dataclasses import dataclass, field
from datetime import date


class OutOfStock(Exception):
    pass


# @dataclass(frozen=True)
@dataclass(unsafe_hash=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


@dataclass
class Batch:
    ref: str
    sku: str
    qty: int
    eta: date = None
    _allocations: set() = field(default_factory=set)

    def __lt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta <= other.eta

    """
    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta
    """

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line) and order_line not in self._allocations:
            self._allocations.add(order_line)
            self.qty -= order_line.qty

    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            self.qty += order_line.qty
            self._allocations.remove(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.sku == order_line.sku and self.qty >= order_line.qty


def allocation(order_line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {order_line.sku}")

    batch.allocate(order_line)

    return batch.ref
    """
    batches = sorted(batches)
    for batch in batches:
        if batch.can_allocate(order_line):
            batch.allocate(order_line)
            return batch.ref
    """
