import asyncio

from typing import Union
from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def throttled(self, target: Union[types.Message, types.CallbackQuery], data: dict):
        handler = current_handler.get()
        if not handler:
            return
        dispatcher = Dispatcher.get_current()
        limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
        key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.target_throttled(target, t, dispatcher, key)
            raise CancelHandler()

    @staticmethod
    async def target_throttled(target: Union[types.Message, types.CallbackQuery],
                                           throttled: Throttled, dispatcher: Dispatcher, key: str):
        message = target.message if isinstance(target, types.CallbackQuery) else target
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count == 2:
            await message.reply("Сликшом часто. Остановись!")
            return
        elif throttled.exceeded_count == 3:
            await message.reply(f"Всё! Больше не отвечу... Осталось: {round(delta, 2)} секунд.")
            return
        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply("Всё, теперь отвечаю")

    async def on_process_message(self, message, data):
        await self.throttled(message, data)

    async def on_process_callback_query(self, call, data):
        await self.throttled(call, data)
