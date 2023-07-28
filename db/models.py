import dataclasses
import uuid
from datetime import date, time
from typing import Optional

UUID = uuid.UUID
Minutes = int


@dataclasses.dataclass
class BotUser:
    telegram_id: int
    full_name: str = None
    birth_date: date = None
    agreement: bool = False
    is_benefits: bool = False

    # def __init__(self,
    #              telegram_id: int,
    #              full_name: str = None,
    #              birth_date: date = None,
    #              agreement: bool = False,
    #              is_benefit: bool = False):
    #     self.telegram_id = telegram_id
    #     self.full_name = full_name
    #     self.birth_date = birth_date
    #     self.agreement = agreement
    #     self.is_benefits = is_benefit


@dataclasses.dataclass
class Service:
    name: str
    cost: int
    duration: Minutes
    id: Optional[UUID] = None
    is_for_benefit: bool = False


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
