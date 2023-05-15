import pytest

import model
import services
import repository


class FakeRepository(repository.AbstractRepository):

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
    line = model.OrderLine("line1", "sku1", 10)
    batch = model.Batch("batch1", "sku1", 100)
    repo = FakeRepository([batch])

    result = services.allocate(line, repo, FakeSession())

    assert result == "batch1"


def test_error_for_invalid_sku():
    line = model.OrderLine("line1", "sku1", 10)
    batch = model.Batch("batch1", "sku2", 100)
    repo = FakeRepository([batch])

    with pytest.raises(services.InvalidSku, match="Invalid sku sku1"):
        services.allocate(line, repo, FakeSession())
    

def test_commits():
    line = model.OrderLine("line1", "sku1", 10)
    batch = model.Batch("batch1", "sku1", 100)
    repo = FakeRepository([batch])

    session = FakeSession()
    ref = services.allocate(line, repo, session)

    assert session.committed
