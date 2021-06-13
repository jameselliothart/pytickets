from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.sql.sqltypes import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
import pytickets.tickets.domain as ticket

mapper_registry = registry()

ticket_table = Table(
    'tickets',
    mapper_registry.metadata,
    Column('status', String(20)),
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column('created_on', DateTime()),
    Column('updated_on', DateTime()),
    Column('summary', String(75)),
    Column('description', String(1000)),
    Column('resolution', String(500)),
    Column('completed_on', DateTime()),
)


def map_entities():
    mapper_registry.map_imperatively(ticket.Ticket,
                                     ticket_table,
                                     polymorphic_on='status',
                                     polymorphic_identity='NotStarted',
                                     )
    mapper_registry.map_imperatively(ticket.InProgress,
                                     ticket_table,
                                     inherits=ticket.Ticket,
                                     polymorphic_identity='InProgress'
                                     )
    mapper_registry.map_imperatively(ticket.Completed,
                                     ticket_table,
                                     inherits=ticket.Ticket,
                                     polymorphic_identity='Completed'
                                     )


def new_session_factory(url, isolation_level="REPEATABLE READ", **kwagrs):
    return sessionmaker(create_engine(url, isolation_level=isolation_level, **kwagrs))
