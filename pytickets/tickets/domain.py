import uuid
from dataclasses import asdict, dataclass, replace
from datetime import datetime, timedelta, timezone
from typing import Any


def as_cst(t: datetime):
    return t.astimezone(timezone(timedelta(hours=-5)))


def now_utc():
    return datetime.now().astimezone(timezone.utc)


@dataclass
class _Metadata():
    updated_on: datetime = None
    created_on: datetime = now_utc()
    id: uuid.uuid4 = uuid.uuid4()

    def replace(self, **changes):
        return replace(self, updated_on=now_utc(), **changes)


@dataclass
class Details():
    summary: str
    description: str = None


@dataclass
class Resolution():
    resolution: str = None
    completed_on: datetime = None


@dataclass
class Ticket(_Metadata, Resolution, Details):
    pass


@dataclass
class InProgress(Ticket):
    pass


@dataclass
class Completed(Ticket):
    pass


@dataclass
class Command():
    pass


@dataclass
class CreateTicket(Command):
    summary: str
    description: str


@dataclass
class CompleteTicket(Command):
    id: uuid.uuid4
    resolution: str
    completed_on: datetime


@dataclass
class Event():
    value: Any


@dataclass
class TicketCreated(Event):
    value: Ticket


@dataclass
class TicketCompleted(Event):
    value: Completed


def new(details: Details):
    return Ticket(**asdict(details))


def not_started(item: Ticket):
    return Ticket(
        **asdict(item.replace(completed_on=None))
    )


def in_progress(item: Ticket):
    return InProgress(
        **asdict(item.replace(completed_on=None))
    )


def complete(item: Ticket, resolution: Resolution):
    return Completed(
        **asdict(item.replace(**asdict(resolution)))
    )


if __name__ == '__main__':
    d = Details('do something')
    ticket = new(d)
    prog = complete(ticket, Resolution('resolved', now_utc()))
    print(prog)
