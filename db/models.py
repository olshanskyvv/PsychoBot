import dataclasses
import datetime
import uuid
from datetime import date, time
from typing import Optional, NamedTuple

UUID = uuid.UUID
Minutes = int


@dataclasses.dataclass
class BotUser:
    telegram_id: int
    full_name: str = None
    birth_date: date = None
    agreement: bool = False
    is_benefits: bool = False


@dataclasses.dataclass
class Service:
    name: str
    cost: int
    duration: Minutes
    id: Optional[UUID] = None
    is_for_benefit: bool = False

    def __str__(self):
        return f'{self.name}: {self.cost} руб'


@dataclasses.dataclass
class AvailableSession:
    date: date
    time_begin: time
    id: Optional[UUID] = None


@dataclasses.dataclass
class Session:
    user: BotUser
    service: Service
    available_session: AvailableSession
    id: Optional[UUID] = None
    is_confirmed: bool = False


class SessionView(NamedTuple):
    id: UUID
    name: str
    date: datetime.date
    time: datetime.time
    is_confirmed: bool
    duration: Minutes
