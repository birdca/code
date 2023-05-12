import abc

from model import Batch


class AbstractRepository(abc.ABC):
    def add(self, batch: Batch):
        raise NotImplementedError

    def get(self) -> Batch:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch: Batch):
        return self.session.add(batch)

    def get(self, ref) -> Batch:
        return self.session.query(Batch).filter_by(ref=ref).one()

    def list(self) -> Batch:
        return self.session.query(Batch).all()
