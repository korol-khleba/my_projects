from aiogram import types, Dispatcher
from utils.create_bot import bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from utils.client import Query


# async def echo_send (message: types.Message, state='*'):

#   await message.reply("Я не распознал твоей команды. Напиши /help.")
# await bot.send_message(message.from_user.id, message.text)


def register_handlers_other(dp: Dispatcher):
    print("")
