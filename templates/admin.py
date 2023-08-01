from db.models import Service

all_services = "Доступные услуги"


def get_service_view_message(service: Service) -> str:
    return f"""{service.name}
Длительность: {service.duration} мин
Стоимость: {service.cost} руб
Льготность: {'Да' if service.is_for_benefit else 'Нет'}"""


def get_service_delete_confirm_message(service: Service) -> str:
    return f"""Вы уверены, что хотите убрать из списка доступных услуг {service.name}?"""
