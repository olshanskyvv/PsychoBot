from db.models import SessionView

no_sessions = """На данный момент у Вас нет запланированных сессий.

Записать Вы можете по команде /new_session"""


def get_session_info_message(session_view: SessionView) -> str:
    return f"""У Вас есть запланированная сессия:

{session_view.name}
{session_view.date.strftime('%d.%m.%Y')} в {session_view.time.strftime('%H:%M')}

Запись{' ' if session_view.is_confirmed else ' не '}подтверждена
"""


session_cancel = """Вы уверены, что хотите отменить сессию?
Если она подтверждена оплатой, средства возвращены не будут"""


