import logging
from typing import Any, Awaitable, Callable, Dict
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import Dispatcher
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.types import Message
from utils.sqlite_db import DataBase


class AuthorizationMiddleware(BaseMiddleware):
    """
    Helps to check if user is authorized to use the bot
    """

    async def on_process_message(self, message: Message, data: dict):
        logging.log(level=logging.INFO, msg=f'[{message.from_user.id}, {message.from_user.full_name}]: {message.text}')
        # Here add user in database
        db = DataBase()
        db.register_user_in_database_if_needed(tg_id=message.from_user.id, username=message.from_user.username)
        # If user not authenticated then CancelMessage and try to subscribe our telegram group
        # raise CancelHandler()
