from db.models import BotUser, UUID, Session
from db.driver import (
    get_user_by_id,
    add_new_user,
    get_id_of_primary_session_service,
    add_new_session
)


async def get_agreement_by_id(telegram_id: int) -> bool:
    user = await get_user_by_id(telegram_id)
    if user:
        return user.agreement
    else:
        await add_new_user(BotUser(telegram_id=telegram_id))
        return False


async def add_new_primary_session(telegram_id: int, av_session_id: UUID) -> UUID:
    primary_service_id = await get_id_of_primary_session_service()
    session_id = await add_new_session(telegram_id=telegram_id,
                                       av_session_id=av_session_id,
                                       service_id=primary_service_id,
                                       is_confirmed=True)
    return session_id
