from aiogram.filters import BaseFilter
from aiogram.types import Message


class UsersFilter(BaseFilter):
    users: tuple[int]

    def __init__(self, *users):
        self.users = tuple(map(int, users))

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.users
