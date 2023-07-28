from db.models import BotUser
from db.driver import get_user_by_id, add_new_user


async def get_agreement_by_id(telegram_id: int) -> bool:
    user = await get_user_by_id(telegram_id)
    if user:
        return user.agreement
    else:
        await add_new_user(BotUser(telegram_id=telegram_id))
        return False

