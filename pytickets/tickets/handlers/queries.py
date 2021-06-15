from sqlalchemy.orm.session import sessionmaker
import pytickets.tickets.domain as ticket


def get_all(session_factory: sessionmaker):
    with session_factory() as session:
        return session.query(ticket.Ticket).all()