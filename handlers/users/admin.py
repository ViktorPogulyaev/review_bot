from aiogram import types

from data.config import ADMINS
from filters import IsPrivate
from loader import dp


@dp.message_handler(IsPrivate(), user_id=ADMINS, text="secret")
async def admit_chat(message: types.Message):
    await message.answer("Вы активиовали секретный админский чат.")
