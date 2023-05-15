from adapters.repository import AbstractRepository
from domain.model import OrderLine, allocation


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    for batch in batches:
        if batch.sku == sku:
            return True
        return False


def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
    batches = repo.list()

    if not is_valid_sku(line.sku, batches):
        raise InvalidSku(f"Invalid sku {line.sku}")

    batchref = allocation(line, batches)
    session.commit()

    return batchref
