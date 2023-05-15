import pytest

from adapters.repository import AbstractRepository
from domain.model import OrderLine, Batch
from service_layer.services import allocate, InvalidSku


class FakeRepository(AbstractRepository):

    def __init__(self, batches):
        self._batches = batches

    def add(self, batch):
        self._batches.add(batch)

    def get(self, ref):
        return next(b for b in self._batches if b.ref == ref)

    def list(self):
        return list(self._batches)


class FakeSession():
    committed = False

    def commit(self):
        self.committed = True


def test_returns_allocation():
    line = OrderLine("line1", "sku1", 10)
    batch = Batch("batch1", "sku1", 100)
    repo = FakeRepository([batch])

    result = allocate(line, repo, FakeSession())

    assert result == "batch1"


def test_error_for_invalid_sku():
    line = OrderLine("line1", "sku1", 10)
    batch = Batch("batch1", "sku2", 100)
    repo = FakeRepository([batch])

    with pytest.raises(InvalidSku, match="Invalid sku sku1"):
        allocate(line, repo, FakeSession())
    

def test_commits():
    line = OrderLine("line1", "sku1", 10)
    batch = Batch("batch1", "sku1", 100)
    repo = FakeRepository([batch])

    session = FakeSession()
    ref = allocate(line, repo, session)

    assert session.committed
