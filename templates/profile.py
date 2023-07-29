import datetime

from db.models import BotUser


def get_profile_data_message(full_name: str, birth_date: datetime.date) -> str:
    return f"""Ваш профиль заполнен:
ФИО: {full_name}
Дата рождения: {birth_date.strftime('%d.%m.%Y')}"""


profile_empty = """Ваш профиль еще не заполнен.
Для начала ввода нажмите кнопку ниже."""


def get_birth_date_message(full_name: str, is_retry: bool = False) -> str:
    string = f"""{full_name}, введите свою дату рождения в формате дд.мм.гггг
    
Пример: 01.01.2000"""
    if is_retry:
        return string + '\n\nНеверный формат. Повторите попытку'
    else:
        return string


def get_confirm_message(full_name: str, birth_date: datetime.date) -> str:
    return f"""Вы ввели:
ФИО: {full_name}
Дата рождения: {birth_date.strftime('%d.%m.%Y')}

Все верно?"""
