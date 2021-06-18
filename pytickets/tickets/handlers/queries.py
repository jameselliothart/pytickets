from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import select
from pytickets.adapters.orm import ticket_table
import pytickets.tickets.domain as ticket


def get_all(session_factory: sessionmaker):
    with session_factory() as session:
        return session.query(ticket.Ticket).all()


def get_open(session_factory: sessionmaker):
    with session_factory() as session:
        stmt = select(ticket_table).where(
            ticket_table.c.status.notin_([ticket.STATUSES[ticket.Completed]])
        )
        return session.execute(stmt).all()
