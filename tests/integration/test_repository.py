from adapters.repository import SqlAlchemyRepository
from domain.model import Batch, OrderLine, allocation


def test_repository_can_save_a_batch(session):
    batch = Batch("batch1", "sku1", 12)

    repo = SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    assert repo.get(batch.ref) == batch


def test_repository_can_retrieve_a_batch_with_allocations(session):
    repo = SqlAlchemyRepository(session)

    order_line = OrderLine("order1", "sku1", 12)
    session.add(order_line)

    batch1 = Batch("batch1", "sku1", 100)
    repo.add(batch1)
    batch2 = Batch("batch2", "sku1", 100)
    repo.add(batch2)
    allocation(order_line, [batch1, batch2])
    session.commit()

    query_batch1 = repo.get("batch1")
    query_batch2 = repo.get("batch2")
    get_al1 = query_batch1._allocations

    assert get_al1 == {order_line}
    assert len(query_batch2._allocations) == 0
