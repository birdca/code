from dataclasses import dataclass, field
from datetime import date


class OutOfStock(Exception):
    pass


@dataclass(frozen=True)
class OrderLine:
    reference: str
    sku: str
    quantity: int


@dataclass
class Batch:
    reference: str
    sku: str
    quantity: int
    eta: date
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
            self.quantity -= order_line.quantity


    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            self._allocations.remove(order_line)


    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.sku == order_line.sku and self.quantity >= order_line.quantity


def allocate(order_line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {order_line.sku}')

    batch.allocate(order_line)

    return batch.reference
    """
    batches = sorted(batches)
    for batch in batches:
        if batch.can_allocate(order_line):
            batch.allocate(order_line)
            return batch.reference
    """
