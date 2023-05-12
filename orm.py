from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from model import Batch, OrderLine

mapper_registry = registry()

"""
order_table = Table(
    "order",
    mapper_registry.metadata,
    Column("id")
)
"""

order_lines = Table(
    "order_lines",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255), nullable=False),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255), nullable=False),
)

batches = Table(
    "batches",
    mapper_registry.metadata,
    Column("ref", String(255), primary_key=True),
    Column("sku", String(255), nullable=False),
    Column("qty", Integer, nullable=False),
    Column("eta", Date, nullable=True),
)

allocations = Table(
    "allocations",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("orderline_id", ForeignKey("order_lines.id")),
    Column("batch_id", ForeignKey("batches.ref")),
)


def start_mappers():
    mapper_registry.map_imperatively(OrderLine, order_lines)
    mapper_registry.map_imperatively(
        Batch,
        batches,
        properties={
            "_allocations": relationship(
                OrderLine, secondary=allocations, collection_class=set
            )
        },
    )
