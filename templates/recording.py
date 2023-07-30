import datetime

from db.models import Minutes

general_choice = 'Выберите тип записи'

date_choice = "Выберите удобную дату для сессии"


def get_time_choice_message(date: datetime.date) -> str:
    return f"Выберите удобное время сессии {date.day}.{date.month}.{date.year}"


def get_confirmation_message(date: datetime.date, time: datetime.time, duration: Minutes) -> str:
    return f"""Вы выбрали сессию {date.strftime('%d.%m.%Y')} в {time.strftime('%H:%M')}.
Она продлиться {duration} минут."""


record_confirmed = """Запись зафиксирована! 
    
Перед сессией Вам придет напоминание со ссылкой на Google Meet конференцию"""

profile_is_empty = """Для записи на вторичную сессию необходимо заполнить ФИО и дату рождения в профиле.

Это можно сделать по команде /profile"""

service_choice = """Выберите тип консультации"""


