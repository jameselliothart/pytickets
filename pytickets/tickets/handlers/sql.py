from dataclasses import asdict
import pytickets.tickets.domain as ticket
from sqlalchemy.orm import sessionmaker


def create_ticket_handler(session_factory: sessionmaker, create_ticket: ticket.CreateTicket):
    details = ticket.Details(create_ticket.summary, create_ticket.description)
    new_ticket = ticket.new(details)
    with session_factory() as session:
        session.add(new_ticket)
        session.commit()
    return ticket.TicketCreated(new_ticket)


def complete_ticket_handler(session_factory: sessionmaker, cmd: ticket.CompleteTicket):
    with session_factory() as session:
        if t := session.query(ticket.Ticket).filter_by(id=cmd.id).first() is not None:
            completed = ticket.complete(t, cmd.resolution)
            session.query(ticket.Ticket).filter_by(id=cmd.id).update(
                status=ticket.STATUSES[ticket.Completed], **asdict(completed))
            session.commit()
    return ticket.TicketCompleted(completed)
