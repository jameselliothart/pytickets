from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.sql.sqltypes import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
import pytickets.tickets.domain as ticket

mapper_registry = registry()

ticket_table = Table(
    'tickets',
    mapper_registry.metadata,
    Column('status', String(ticket.SCHEMA['status'])),
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column('created_on', DateTime()),
    Column('updated_on', DateTime()),
    Column('summary', String(ticket.SCHEMA['summary'])),
    Column('description', String(ticket.SCHEMA['description'])),
    Column('resolution', String(ticket.SCHEMA['resolution'])),
    Column('completed_on', DateTime()),
)


def new_session_factory(url, isolation_level="REPEATABLE READ", **kwagrs):
    return sessionmaker(create_engine(url, isolation_level=isolation_level, **kwagrs))


def get_all(session_factory: sessionmaker):
    with session_factory() as session:
        return session.query(ticket.Ticket).all()


def get_open(session_factory: sessionmaker):
    with session_factory() as session:
        stmt = select(ticket_table).where(
            ticket_table.c.status.notin_([ticket.STATUSES[ticket.Completed]])
        )
        return session.execute(stmt).all()


def map_entities():
    mapper_registry.map_imperatively(ticket.Ticket,
                                     ticket_table,
                                     polymorphic_on='status',
                                     polymorphic_identity=ticket.STATUSES[ticket.Ticket],
                                     )
    mapper_registry.map_imperatively(ticket.InProgress,
                                     ticket_table,
                                     inherits=ticket.Ticket,
                                     polymorphic_identity=ticket.STATUSES[ticket.InProgress]
                                     )
    mapper_registry.map_imperatively(ticket.Completed,
                                     ticket_table,
                                     inherits=ticket.Ticket,
                                     polymorphic_identity=ticket.STATUSES[ticket.Completed]
                                     )
