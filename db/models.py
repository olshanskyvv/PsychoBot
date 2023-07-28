from datetime import date, time

UUID = str
Minutes = int


class BotUser:
    telegram_id: int
    birth_date: date
    agreement: bool
    is_benefit: bool


class Service:
    id: UUID
    name: str
    cost: int
    duration: Minutes
    is_for_benefit: bool


class AvailableSession:
    id: UUID
    date: date
    time_begin: time


class Session:
    id: UUID
    user: BotUser
    service: Service
    available_session: AvailableSession
    is_confirmed: bool

