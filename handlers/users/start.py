from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Здесь ты можешь оставить свой отзыв о нашем продукте. "
                         f"Мы будем очень рады! ")
