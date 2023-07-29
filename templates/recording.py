import datetime

general_choice = 'Выберите тип записи'

date_choice = "Выберите удобную дату для сессии"


def get_time_choice_message(date: datetime.date) -> str:
    return f"Выберите удобное время сессии {date.day}.{date.month}.{date.year}"


def get_primary_confirmation_message(date: datetime.date, time: datetime.time) -> str:
    return f"""Вы выбрали первичную сессию {date.day}.{date.month}.{date.year} в {time.hour}:{time.minute}.
Она продлиться 30 минут."""


primary_record_confirmed = """Запись зафиксирована! 
    
Перед сессией Вам придет напоминание со ссылкой на Google Meet конференцию"""
