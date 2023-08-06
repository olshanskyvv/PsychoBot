from db.models import Service, SessionFullView

all_services = "Доступные услуги"


def get_service_view_message(service: Service) -> str:
    return f"""{service.name}
Длительность: {service.duration} мин
Стоимость: {service.cost} руб
Льготность: {'Да' if service.is_for_benefit else 'Нет'}"""


def get_service_delete_confirm_message(service: Service) -> str:
    return f"""Вы уверены, что хотите убрать из списка доступных услуг {service.name}?"""


def get_session_view_message(session: SessionFullView) -> str:
    return f"""{session.service_name}
Запланирована на {session.date.strftime('%d.%m.%Y')} {session.time.strftime('%H:%M')}

Клиент:
ФИО - {session.full_name}
Дата рождения - {session.user_birth.strftime('%d.%m.%Y')}
Тег - @{session.username}

Сессия {'' if session.is_confirmed else 'не '}оплачена (подтверждена)
"""



