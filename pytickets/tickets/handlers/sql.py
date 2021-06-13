from dataclasses import asdict
import pytickets.tickets.domain as ticket
from sqlalchemy.orm import sessionmaker


def new_create_ticket_handler(session_factory: sessionmaker):
    def _create_ticket_handler(create_ticket: ticket.CreateTicket):
        details = ticket.Details(
            create_ticket.summary, create_ticket.description)
        new_ticket = ticket.new(details)
        with session_factory() as session:
            session.add(new_ticket)
            session.commit()
        return ticket.TicketCreated(new_ticket)
    return _create_ticket_handler


def new_complete_ticket_handler(session_factory: sessionmaker):
    def _complete_ticket_handler(cmd: ticket.CompleteTicket):
        with session_factory() as session:
            t = session.query(ticket.Ticket).filter_by(id=cmd.id).first()
            if t is not None:
                completed = ticket.complete(t, cmd.resolution)
                session.query(ticket.Ticket).filter_by(id=cmd.id).delete()
                session.add(completed)
                session.commit()
        return ticket.TicketCompleted(completed)
    return _complete_ticket_handler
