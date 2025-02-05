from utils import client, other
import aiogram.utils as ut
from aiogram.utils import executor
from utils.create_bot import dp, bot
from asyncio import create_task
import logging
import sys
from utils.common_utils import get_subscribed_users, send_daily_message
from utils.authentication import AuthorizationMiddleware
from utils.sqlite_db import DataBase

async def on_startup(_):  # info about start bot
    logging.log(level=logging.INFO, msg='Bot has been started')
    db = DataBase ()
    for user_id in db.get_admins_tg_ids ():
        try:
            await bot.send_message(user_id, "Bot has been started")
        except ut.exceptions.BotBlocked:
            print(f'User: {user_id} blocked this bot')
    users = get_subscribed_users()
    for user_id in users:
        create_task(send_daily_message(user_id))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    dp.setup_middleware(AuthorizationMiddleware())
    client.register_handlers_client(dp)  # Events from user
    other.register_handlers_other(dp)  # Other events
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
