from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import UUID, SessionView, Minutes
from utils.callback_factories import SessionActionFactory, SessionAction


def get_session_info_keyboard(session_view: SessionView) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if session_view.is_confirmed:
        builder.button(text='Перенести',
                       callback_data=SessionActionFactory(id=session_view.id,
                                                          duration=session_view.duration,
                                                          action=SessionAction.MOVE))
    else:
        builder.button(text='Оплатить',
                       callback_data=SessionActionFactory(id=session_view.id,
                                                          duration=session_view.duration,
                                                          action=SessionAction.PAY))

    builder.button(text='Отменить',
                   callback_data=SessionActionFactory(id=session_view.id,
                                                      duration=session_view.duration,
                                                      action=SessionAction.CANCEL))
    builder.adjust(1)
    return builder.as_markup()


def get_session_cancel_confirm_keyboard(session_id: UUID, duration: Minutes) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Не отменять',
                   callback_data='session_cancel_confirm_fail')
    builder.button(text='Отменить',
                   callback_data=SessionActionFactory(id=session_id,
                                                      duration=duration,
                                                      action=SessionAction.CANCEL_CONFIRM))
    builder.adjust(1)
    return builder.as_markup()
