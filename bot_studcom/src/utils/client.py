import os
import json
import config
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from utils.common_utils import get_subscribed_users, get_subscription_status, send_daily_message, \
    set_subscription_status
from utils.common_utils import subs_notify
from utils.create_bot import dp, bot
from utils.create_bot import database_table, other_data_table, food_ds_table, shop_ds_table, admin_ds_table
from utils.sqlite_db import DataBase

async def commands_start(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    start_message = other_data_table['values'][1][2]
    await bot.send_message(message.from_user.id, start_message, parse_mode=types.ParseMode.HTML)


async def commands_help(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    with open(config.FileLocation.cmd_help, 'r', encoding='utf-8') as file:
        await bot.send_message(message.from_user.id, file.read(), parse_mode=types.ParseMode.HTML)


async def commands_horo_help(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    with open(config.FileLocation.cmd_horo_help, 'r', encoding='utf-8') as file:
        await bot.send_message(message.from_user.id, file.read(), parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=['restart'], state='*')
async def restart_bot(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    db = DataBase ()
    admins_list = db.get_admins_tg_ids ()
    if (message.from_user.id not in admins_list):
        await bot.send_message(message.from_user.id, "У вас нет доступа к рестарту бота!\n")
        return

    await bot.send_message(message.from_user.id, 'Restarting bot')
    for user_id in admins_list:
        if message.from_user.id != user_id:
            try:
                await bot.send_message(user_id,
                                       'User {} requested a restart of the bot!'.format(message.from_user.full_name))
            except:
                print(f'Cannot send message to {user_id}')
    curr_path_to_script = os.getcwd()
    print(f"Restarting {curr_path_to_script}")
    quit(os.system('python3 ' + curr_path_to_script + '/main.py'))


async def echo_error(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    await message.reply("Я не распознал твоей команды. Напиши /help.")


async def commands_feedback(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    split = message.text.split(' ', 1)
    if len(split) > 1:
        db = DataBase ()
        admins_list = db.get_admins_tg_ids ()
        await subs_notify(admins_list,
                          'Обратная связь от \n@{}\n{}:\n{}'.format(message.from_user.username,
                                                                    message.from_user.full_name, split[1]))
        await bot.send_message(message.from_user.id, "Фидбек отправлен!")
    else:
        await bot.send_message(message.from_user.id, "/feedback [ваше обращение]")


class Query(StatesGroup):
    building = State()
    corpus = State()
    floor = State()


def create_list_buildings(building):
    corpus_list = []
    A_corpus = InlineKeyboardButton(text='А', callback_data='Корпус А')
    B_corpus = InlineKeyboardButton(text='Б', callback_data='Корпус Б')
    V_corpus = InlineKeyboardButton(text='В', callback_data='Корпус В')
    G_corpus = InlineKeyboardButton(text='Г', callback_data='Корпус Г')
    E_corpus = InlineKeyboardButton(text='Е', callback_data='Корпус Е')
    ZHE_corpus = InlineKeyboardButton(text='Ж', callback_data='Корпус Ж')
    D_corpus = InlineKeyboardButton(text='Д', callback_data='Корпус Д')
    if (building == 'ДСЛ'):
        corpus_list = [A_corpus, B_corpus]
    if (building == 'ДС'):
        corpus_list = [B_corpus, V_corpus, G_corpus,
                       D_corpus, E_corpus, ZHE_corpus]
    return corpus_list


def build_back_button():
    return InlineKeyboardButton(text='Назад', callback_data='Back')


def build_next_button():
    return InlineKeyboardButton(text='Продолжить➡️', callback_data='Next')


def build_finish_button():
    return InlineKeyboardButton(text='🧸 Результат', callback_data='View_Information')


def build_cancel_button():
    return InlineKeyboardButton(text='❌ Скрыть', callback_data='Cancel')


def build_choose_building_button():
    keyboard_build_query = InlineKeyboardMarkup(row_width=16)
    gz_button = InlineKeyboardButton(text='ДС', callback_data='ДС')
    dsl_button = InlineKeyboardButton(text='ДСЛ', callback_data='ДСЛ')
    return keyboard_build_query.row(gz_button, dsl_button).row(build_cancel_button())


def build_choose_corpus_button(building):
    keyboard_build_query = InlineKeyboardMarkup(row_width=3)
    list_corpus = create_list_buildings(building)
    return keyboard_build_query.row(
        *list_corpus).row(build_cancel_button())


def build_choose_floor_button(corpus, building):
    keyboard_build_query_floor = InlineKeyboardMarkup(row_width=20)
    floor_1 = InlineKeyboardButton(text='1', callback_data='Этаж 1')
    floor_2 = InlineKeyboardButton(text='2', callback_data='Этаж 2')
    floor_3 = InlineKeyboardButton(text='3', callback_data='Этаж 3')
    floor_4 = InlineKeyboardButton(text='4', callback_data='Этаж 4')
    floor_5 = InlineKeyboardButton(text='5', callback_data='Этаж 5')
    floor_6 = InlineKeyboardButton(text='6', callback_data='Этаж 6')
    floor_7 = InlineKeyboardButton(text='7', callback_data='Этаж 7')
    floor_8 = InlineKeyboardButton(text='8', callback_data='Этаж 8')
    floor_9 = InlineKeyboardButton(text='9', callback_data='Этаж 9')
    floor_10 = InlineKeyboardButton(text='10', callback_data='Этаж 10')
    floor_11 = InlineKeyboardButton(text='11', callback_data='Этаж 11')
    floor_12 = InlineKeyboardButton(text='12', callback_data='Этаж 12')
    floor_13 = InlineKeyboardButton(text='13', callback_data='Этаж 13')
    floor_14 = InlineKeyboardButton(text='14', callback_data='Этаж 14')
    floor_15 = InlineKeyboardButton(text='15', callback_data='Этаж 15')
    floor_16 = InlineKeyboardButton(text='16', callback_data='Этаж 16')
    floor_17 = InlineKeyboardButton(text='17', callback_data='Этаж 17')
    floor_18 = InlineKeyboardButton(text='18', callback_data='Этаж 18')
    floor_19 = InlineKeyboardButton(text='19', callback_data='Этаж 19')
    floor_20 = InlineKeyboardButton(text='20', callback_data='Этаж 20')
    floor_21 = InlineKeyboardButton(text='21', callback_data='Этаж 21')
    floor_22 = InlineKeyboardButton(text='22', callback_data='Этаж 22')
    floor_23 = InlineKeyboardButton(text='23', callback_data='Этаж 23')
    list_floor = []
    if (building == 'ДСЛ'):
        if corpus == 'А':
            list_floor = [floor_9, floor_10, floor_11, floor_12]
        elif corpus == 'Б':
            list_floor = [floor_8, floor_9, floor_10]
        return keyboard_build_query_floor.row(*list_floor).row(build_cancel_button())
    elif building == 'ДС':
        if corpus in ['Б', 'В']:
            floor_list_1 = [floor_3, floor_4, floor_5,
                            floor_6, floor_7, floor_8, floor_9, floor_10]
            floor_list_2 = [floor_11, floor_13, floor_14, floor_15, floor_16, floor_17,
                            floor_18, floor_20]
            floor_list_3 = [floor_21, floor_22, floor_23]
            return keyboard_build_query_floor.row(*floor_list_1).row(*floor_list_2).row(*floor_list_3).row(
                build_cancel_button())
        elif corpus in ['Г', 'Е', 'Ж', 'Д']:
            floor_list_1 = [floor_1, floor_2, floor_3, floor_4]
            floor_list_2 = [floor_5, floor_6, floor_7, floor_8, floor_9]
        return keyboard_build_query_floor.row(*floor_list_1).row(*floor_list_2).row(build_cancel_button())


async def commands_get_information(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    print("Kill state")
    await message.reply('Выбери Общежитие:⤵️', reply_markup=build_choose_building_button())
    await Query.building.set()


def build_choose_dsl_gz_wash_button():
    keyboard_build_query = InlineKeyboardMarkup(row_width=16)
    gz_button = InlineKeyboardButton(text='ДС', callback_data='ds_wash')
    dsl_button = InlineKeyboardButton(text='ДСЛ', callback_data='dsl_wash')
    return keyboard_build_query.row(gz_button, dsl_button).row(build_cancel_button())


@dp.callback_query_handler(lambda c: c.data in ['ds_wash', 'dsl_wash'], state='*')
async def view_ds_wash(callback: types.CallbackQuery, state: FSMContext):
    curr_data = callback.data
    if (curr_data == 'ds_wash'):
        text = other_data_table['values'][1][0]
    else:  # dsl_wash_case
        text = other_data_table['values'][1][1]

    keyboard_build_query = InlineKeyboardMarkup(row_width=16)
    await callback.message.edit_text(text, parse_mode=types.ParseMode.HTML,
                                     reply_markup=keyboard_build_query.row(build_cancel_button()))


async def commands_wash_clothes(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    await message.reply('Выбери Общежитие:⤵️', reply_markup=build_choose_dsl_gz_wash_button())


async def commands_recycle_dsl(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    recycle_dsl_text = other_data_table['values'][1][4]
    await bot.send_message(message.from_user.id, recycle_dsl_text, parse_mode=types.ParseMode.HTML,
                           reply_markup=build_cancel_button())


async def commands_gym_dsl(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    gym_text = other_data_table['values'][1][5]
    await bot.send_message(message.from_user.id, gym_text, parse_mode=types.ParseMode.HTML,
                           reply_markup=build_cancel_button())


@dp.callback_query_handler(Text(startswith='Cancel'), state='*')
async def close_view_data(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.reset_data()
    await callback.answer('✅ Просмотр информации скрыт')
    await callback.message.delete()


def build_view_information_page():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard_comenda = InlineKeyboardButton(
        text='Моя коменда', callback_data='comenda_dezhurnii')
    keyboard_proverka = InlineKeyboardButton(
        text='Расписание проверок', callback_data='room_check_time')
    keyboard_starosta = InlineKeyboardButton(
        text='Старосты моего этажа', callback_data='starosta_floors')
    list_functions = [keyboard_comenda, keyboard_proverka, keyboard_starosta]
    return keyboard.add(keyboard_comenda, keyboard_proverka, keyboard_starosta, build_cancel_button())


@dp.callback_query_handler(Text(startswith='starosta_floors'), state='*')
async def show_room_check_time(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if (len(data) < 3):
            await callback.answer(text='⚠️ Введите данные заново. Нажмите Выход\Скрыть.')
            return

    await callback.answer(text='🕐Получаю информацию...')
    last_data_update = database_table['values'][1][16]
    for row_data in database_table['values']:
        if (row_data[0] == data['building'] and row_data[1] == data['corpus'] and int(row_data[2]) <= int(
                data['floor']) and int(row_data[3]) >= int(data['floor'])):
            print("row_data[2]:{} row_data[3]:{} data['floor']:{}".format(
                row_data[2], row_data[3], data['floor']))
            print(row_data)
            print("LEN:" + str(len(row_data)))
            if (len(row_data) > 10):
                starosta1 = row_data[10]
            else:
                starosta1 = ''
            if (len(row_data) > 11):
                link1 = row_data[11]
            else:
                link1 = ''
            if (len(row_data) > 12):
                starosta2 = row_data[12]
            else:
                starosta2 = ''
            if (len(row_data) > 13):
                link2 = row_data[13]
            else:
                link2 = ''
            if (len(row_data) > 15):
                starosta3 = row_data[14]
            else:
                starosta3 = ''
            if (len(row_data) == 16):
                link3 = row_data[15]
            else:
                link3 = ''

    with open(config.FileLocation.cmd_my_starosta, 'r', encoding='utf-8') as file:
        nice = file.read()
    text = nice.format(starosta_1=starosta1, link_1=link1, starosta_2=starosta2,
                       link_2=link2, starosta_3=starosta3, link_3=link3)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(build_back_to_view_information(), build_cancel_button())
    await callback.message.edit_text(text=text, parse_mode=types.ParseMode.HTML, reply_markup=keyboard,
                                     disable_web_page_preview=True)


@dp.callback_query_handler(Text(startswith='room_check_time'), state='*')
async def show_room_check_time(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if (len(data) < 3):
            await callback.answer(text='⚠️ Введите данные заново. Нажмите Выход\Скрыть.')
            return
    await callback.answer(text='🕐Получаю информацию...')

    last_data_update = database_table['values'][1][16]
    for row_data in database_table['values']:
        if (row_data[0] == data['building'] and row_data[1] == data['corpus'] and int(row_data[2]) <= int(
                data['floor']) and int(row_data[3]) >= int(data['floor'])):
            print("row_data[2]:{} row_data[3]:{} data['floor']:{}".format(
                row_data[2], row_data[3], data['floor']))
            print(row_data)
            check_rooms_time = row_data[9]
    with open(config.FileLocation.cmd_check_rooms_time, 'r', encoding='utf-8') as file:
        nice = file.read()
    text = nice.format(check_rooms_range_time=check_rooms_time)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(build_back_to_view_information(), build_cancel_button())
    await callback.message.edit_text(text=text, parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='comenda_dezhurnii'), state='*')
async def show_comenda(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if (len(data) < 3):
            await callback.answer(text='⚠️ Введите данные заново. Нажмите Выход\Скрыть.')
            return
    await callback.answer(text='🕐Получаю информацию...')

    last_data_update = database_table['values'][1][16]
    for row_data in database_table['values']:
        if (row_data[0] == data['building'] and row_data[1] == data['corpus'] and int(row_data[2]) <= int(
                data['floor']) and int(row_data[3]) >= int(data['floor'])):
            print("row_data[2]:{} row_data[3]:{} data['floor']:{}".format(
                row_data[2], row_data[3], data['floor']))
            print(row_data)
            comenda_name = row_data[4]
            comenda_room = row_data[5]
            comenda_work_time = row_data[6]
            dezhurnii_phone = row_data[7]
            dezhurnii_room = row_data[8]
    with open(config.FileLocation.cmd_comenda_info, 'r', encoding='utf-8') as file:
        nice = file.read()
    text = nice.format(comenda_name=comenda_name, comenda_room=comenda_room, comenda_work_time=comenda_work_time,
                       dezhurnii_phone=dezhurnii_phone, dezhurnii_room=dezhurnii_room,
                       last_data_update=last_data_update)
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.row(build_back_to_view_information(), build_cancel_button())
    await callback.message.edit_text(text=text, parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


def build_back_to_view_information():
    return InlineKeyboardButton(text='⬅️ Назад', callback_data='View_Information')


@dp.callback_query_handler(Text(startswith='View_Information'), state='*')
async def view_information_fun(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if (len(data) < 3):
            await callback.answer(text='⚠️ Вы ничего не выбрали')
            await callback.message.answer(
                text='Выберите данные или нажмите Выход\Скрыть, а затем введите команду заново.')
            return
    await callback.answer(
        "✅ Открываю страницу с информацией для + " + data['building'] + data['corpus'] + str(data['floor']) + "...")
    await callback.message.edit_text(text='Выбери, что ты хочешь узнать:', reply_markup=build_view_information_page())


@dp.callback_query_handler(Text(startswith='Next'), state='*')
async def set_next_state(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()

    print("callback data:" + callback.data)
    print("cur_state:" + current_state)
    if (current_state == None):
        return

    async with state.proxy() as data:
        if (current_state == Query.building.state):  # Building to Corpus
            print("Building to corpus:")
            if (len(data) != 1):
                await callback.answer(text='⚠️ Вы ничего не выбрали')
                return
            keyboard = build_choose_corpus_button(data['building'])
            await callback.message.edit_text(text='Выбери Корпус:⤵️', reply_markup=keyboard)
            await Query.corpus.set()
        if (current_state == Query.corpus.state):  # Corpus to floor
            print("Corpus to floor")
            if (len(data) < 2):
                await callback.answer(text='⚠️ Вы ничего не выбрали')
                return
            keyboard = build_choose_floor_button(
                data['corpus'], data['building'])
            await callback.message.edit_text(text='Выбери Этаж:⤵️', reply_markup=keyboard)
            await Query.floor.set()
    print("NOT here")


@dp.callback_query_handler(lambda call: call.data == 'ДСЛ' or call.data == 'ДС', state=Query.building)
async def set_state_building(callback: types.CallbackQuery, state: FSMContext):
    building = callback.data
    async with state.proxy() as data:
        data['building'] = building
    print(data['building'])
    await callback.answer("✅ Выбрано {}".format(building))
    await set_next_state(callback, state)


@dp.callback_query_handler(Text(startswith='Корпус'), state=Query.corpus)
async def set_corpus(callback: types.CallbackQuery, state: FSMContext):
    corpus = callback.data.split(' ')[1]
    async with state.proxy() as data:
        data['corpus'] = corpus
    print("corpus:" + data['corpus'] + "|" + "building:" + data['building'])
    await callback.answer("✅ Выбрано {}".format(data['corpus']))
    await set_next_state(callback, state)


@dp.callback_query_handler(Text(startswith='Этаж'), state=Query.floor)
async def set_floor(callback: types.CallbackQuery, state: FSMContext):
    floor = callback.data.split(' ')[1]
    print(floor)
    async with state.proxy() as data:
        data['floor'] = int(floor)

    print("corpus:" + data['corpus'] + "|" + "building:" +
          data['building'] + "floor:" + str(data['floor']))

    await callback.answer("✅ Выбрано {}".format(data['floor']))
    await view_information_fun(callback, state)


@dp.callback_query_handler(Text(startswith='Back'), state='*')
async def set_back(callback: types.CallbackQuery, state: FSMContext):
    state_now = await state.get_state()
    if (state_now == Query.corpus.state):  # From corpus to building
        print("From corpus to building")
        await Query.building.set()
        await commands_get_information(callback.message, state)
    elif (state_now == Query.floor.state):  # From floor to corpus
        print("From floor to corpus")
        async with state.proxy() as data:
            list_corpus = create_list_buildings(data['building'])
        keyboard_build_query = InlineKeyboardMarkup(row_width=3)
        keyboard_build_query.row(
            *list_corpus).insert(InlineKeyboardButton(text="Назад", callback_data='Back'))
        await callback.message.edit_text(text='Выбери корпус:', reply_markup=keyboard_build_query)
        await callback.answer("✅ Choosed {}".format(building))
        await Query.corpus.set()
    print(state_now)
    print(Query.floor.state)
    print("not here")


async def echo_error(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    await message.reply("Я не распознал твоей команды. Напиши /help.")


async def commands_rasselenie(message: types.Message, state: FSMContext):
    await state.finish()
    await state.reset_data()
    inspektor = other_data_table['values'][1][3]
    await bot.send_message(message.from_user.id, inspektor, parse_mode=types.ParseMode.HTML,
                           reply_markup=build_cancel_button())


async def food_command(message: types.Message, state='*'):
    keyboard_build_query = InlineKeyboardMarkup(row_width=16)
    curr_data = message.text
    match curr_data:
        case '/food':
            clb_data = 'food'
        case '/shop':
            clb_data = 'shop'
        case '/admin_ds':
            keyboard = build_choose_button('admin_ds', database['ДС']['admin_ds'])
            await message.reply('Выбери нужный вариант:⤵️', parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
            return

    gz_button = InlineKeyboardButton(text='ДС', callback_data=f'ds_{clb_data}')
    dsl_button = InlineKeyboardButton(text='ДСЛ', callback_data=f'dsl_{clb_data}')
    await bot.send_message(message.from_user.id, 'Выбери нужный вариант:⤵️', parse_mode=types.ParseMode().HTML,
                           reply_markup=keyboard_build_query.row(gz_button, dsl_button).row(build_cancel_button()))


@dp.callback_query_handler(lambda c: c.data in ['ds_food', 'dsl_food', 'ds_shop', 'dsl_shop'], state='*')
async def build_info_ds(callback: types.CallbackQuery, state='*'):
    await state.finish()
    await state.reset_data()
    curr_data = callback.data
    keyboard = InlineKeyboardMarkup(width=15)
    match curr_data:
        case 'ds_shop':
            keyboard = build_choose_button('shop_ds', database['ДС']['shop_ds'])
        case 'ds_food':
            keyboard = build_choose_button('food_ds', database['ДС']['food_ds'])
        case 'dsl_shop':
            keyboard = build_choose_button('shop_dsl', database['ДСЛ']['shop_dsl'])
        case 'dsl_food':
            keyboard = build_choose_button('food_dsl', database['ДСЛ']['food_dsl'])

    await callback.message.edit_text('Выбери нужный вариант:⤵️', parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


ds_shop = {
    'shop_B': {
        'name': 'Магазин Б',
        'text': shop_ds_table['values'][1][0],
    },
    'shop_V': {
        'name': 'Магазин В',
        'text': shop_ds_table['values'][1][1],
    },
    'apteka_B': {
        'name': 'Аптека Б',
        'text': shop_ds_table['values'][1][2],
    },
    'argument': {
        'name': 'Аргумент',
        'text': shop_ds_table['values'][1][3],
    },
    'meat_dep': {
        'name': 'Мясной отдел',
        'text': shop_ds_table['values'][1][4],
    },
    'chai_shop_b': {
        'name': 'Чай Б',
        'text': shop_ds_table['values'][1][5],
    },
    'but_home': {
        'name': 'Дом Быта',
        'text': shop_ds_table['values'][1][6],
    },
    'beaty_shop': {
        'name': 'Салон красоты',
        'text': shop_ds_table['values'][1][7],
    }
}

ds_food = {
    'stolovaya_1': {
        'name': 'Столовая Б',
        'text': food_ds_table['values'][1][0],
    },
    'dietka': {
        'name': 'Диетка',
        'text': food_ds_table['values'][1][1],
    },
    'pizza_ds': {
        'name': 'Пицца',
        'text': food_ds_table['values'][1][2],
    },
    'professor': {
        'name': 'Профессоркая',
        'text': food_ds_table['values'][1][3],
    },
    'cafe_fakultet': {
        'name': 'Факультет',
        'text': food_ds_table['values'][1][4],
    },
    'shaiba': {
        'name': 'Шайба',
        'text': food_ds_table['values'][1][5],
    },
    'konditer': {
        'name': 'Кондитерская',
        'text': food_ds_table['values'][1][6],
    }
}

ds_administration = {
    'passport_table': {
        'name': 'Паспортный Стол',
        'text': admin_ds_table['values'][1][0],
    },
    'pass_office': {
        'name': 'Бюро Пропусков',
        'text': admin_ds_table['values'][1][1],
    },
    'police': {
        'name': 'Полиция',
        'text': admin_ds_table['values'][1][2],
    },
    'post_office': {
        'name': 'Почта',
        'text': admin_ds_table['values'][1][3],
    },
    'UOBF': {
        'name': 'УОБФ',
        'text': admin_ds_table['values'][1][4],
    },
}

dsl_food = {
    'stolovaya_v_corpus': {
        'name': 'Столовая В.102',
        'text': food_ds_table['values'][1][7]
    }
}

dsl_shop = {
    'campus_market': {
        'name': 'Кампус Маркет',
        'text': shop_ds_table['values'][1][8]
    }
}

database = {
    'ДС': {
        'admin_ds': ds_administration,
        'shop_ds': ds_shop,
        'food_ds': ds_food,
    },
    'ДСЛ': {
        'shop_dsl': dsl_shop,
        'food_dsl': dsl_food,
    }
}


def build_choose_button(object_type, objects_list):
    keyboard_build_query = InlineKeyboardMarkup(row_width=16)
    btn = {}
    for elem in objects_list:
        btn[objects_list[elem]['name']] = InlineKeyboardButton(text=objects_list[elem]['name'], callback_data=elem)
    print(btn)
    match object_type:
        case 'food_ds':
            keyboard = keyboard_build_query.row(btn['Столовая Б'], btn['Диетка']).row(btn['Пицца'], btn['Шайба']).row(
                btn['Профессоркая']).row(btn['Кондитерская']).row(btn['Факультет'])
        case 'shop_ds':
            keyboard = keyboard_build_query.row(btn['Магазин Б'], btn['Магазин В']).row(btn['Аптека Б'],
                                                                                        btn['Аргумент']).row(
                btn['Чай Б'], btn['Мясной отдел']).row(btn['Дом Быта'], btn['Салон красоты'])
        case 'admin_ds':
            keyboard = keyboard_build_query.row(btn['Паспортный Стол']).row(btn['Бюро Пропусков']).row(
                btn['Полиция']).row(btn['Почта']).row(btn['УОБФ'])
        case 'shop_dsl':
            keyboard = keyboard_build_query.row(btn['Кампус Маркет'])
        case 'food_dsl':
            keyboard = keyboard_build_query.row(btn['Столовая В.102'])

    return keyboard.row(build_cancel_button())


@dp.callback_query_handler(
    lambda c: c.data in ds_food or c.data in ds_shop or c.data in ds_administration or c.data in dsl_food or c.data in dsl_shop,
    state='*')
async def view_ds_information(callback: types.CallbackQuery, state: FSMContext):
    curr_data = callback.data
    print(curr_data)
    if (curr_data in ds_food):
        db = ds_food
    elif (curr_data in ds_shop):
        db = ds_shop
    elif (curr_data in ds_administration):
        db = ds_administration
    elif (curr_data in dsl_shop):
        db = dsl_shop
    elif (curr_data in dsl_food):
        db = dsl_food
    text = db[callback.data]['text']
    keyboard_build_query = InlineKeyboardMarkup(row_width=16)
    await callback.message.edit_text(text, parse_mode=types.ParseMode.HTML,
                                     reply_markup=keyboard_build_query.row(build_cancel_button()))


async def subscribe_horo(message: types.Message):
    user_id = message.from_user.id
    sub_users = get_subscribed_users()
    print('subs:' + str(sub_users))
    print('status:' + str(get_subscription_status(user_id)))
    if str(user_id) in sub_users and get_subscription_status(user_id) == True:
        await message.answer('Вы уже получаете ежедневные сообщения (:')
        return

    set_subscription_status(user_id, True)
    with open(config.FileLocation.time_json, 'r') as file:
        time_res = json.load(file)
    hour = time_res['hour']
    minute = time_res['minutes']
    await message.answer(f'Теперь каждое утро в {hour} : {minute} я буду присылать свои отобранные открытки 🥰🥳')
    await send_daily_message(user_id)


async def unsubscribe_horo(message: types.Message):
    user_id = message.from_user.id
    set_subscription_status(user_id, False)
    await message.answer("Теперь я не буду присылать каждое утро тебе открытку :(")


async def set_time_horo(message: types.Message):
    data = (message.text)
    res = data.split(' ')
    if (len(res) != 3):
        await message.answer("Попробуй пожалуйста /horo_time hour minutes")
        return
    hour = res[1]
    minute = res[2]
    if res[1].isdigit() and res[2].isdigit() and int(hour) >= 0 and int(hour) <= 23 and int(minute) >= 0 and int(
            minute) <= 59:
        file = open(config.FileLocation.time_json, 'w')
        res_time = {}
        res_time['hour'] = hour
        res_time['minutes'] = minute
        json.dump(res_time, file)
        await message.answer(f"Теперь я буду желать тебе самого доброго утра в {hour}:{minute} 🥰🥳")
    else:
        await message.answer("Попробуй пожалуйста /horo_time hour minutes цифрами.\nExample: /horo_time 13 44")


async def set_admin_for_user(message: types.Message, state='*'):
    await state.finish()
    await state.reset_data()

    data = message.text.split(' ')
    if (len(data) != 3):
        await message.answer('Используйте /set_admin <username> <1 или 0>\nПример: /set_admin vls4m 1')
        return

    if (not data[2].isdigit()):
        await message.answer('Используйте /set_admin <username> <1 или 0>\nПример: /set_admin vls4m 1')
        return
    is_admin = int(data[2])
    if not (is_admin >= 0 and is_admin <= 1):
        await message.answer('Используйте /set_admin <username> <1 или 0>\nПример: /set_admin vls4m 1')
        return

    db = DataBase()
    res = db.set_admin_for_user(message.from_user.id, data[1], is_admin)
    # TODO: Notify user which state is_admin has been changed.
    # TODO: Notify all admins who changed admin mode about user
    await message.answer(
        f'Результат добавления пользователем {message.from_user.username} администратора {data[1]}: {res}')


async def help_admin (message: types.Message, state='*'):
    await state.finish()
    await state.reset_data()
    with open(config.FileLocation.admin_help, 'r', encoding='utf-8') as file:
        await bot.send_message(message.from_user.id, file.read(), parse_mode=types.ParseMode.HTML)

class Form(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirmation = State()


async def notify_all_users(message: types.Message, state='*'):
    await state.finish()
    await state.reset_data()
    await Form.waiting_for_message.set()
    await message.reply(
        "Пожалуйста, введите ваше сообщение. Если хотите добавить изображение, отправьте его после текста.")


@dp.message_handler(state=Form.waiting_for_message, commands='confirm')
async def confirm_send(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    text_msg = user_data.get('text', '')
    photo_id = user_data.get('photo')


    # Добавляем клавиатуру с кнопками "Подтвердить" и "Отменить"
    keyboard_build_query = InlineKeyboardMarkup(row_width=3, one_time_keyboard=True)
    confirm_button = InlineKeyboardButton (text='Подтвердить', callback_data='Confirm')
    cancel_button = InlineKeyboardButton (text='Отменить', callback_data='StopMsg')
    keyboard_build_query.row (confirm_button, cancel_button)
    # Уведомляем пользователя о сообщении
    if photo_id:
        await message.answer_photo(photo=photo_id, caption=text_msg)
    else:
        await message.answer(text_msg)

    await Form.waiting_for_confirmation.set()  # Переход к следующему состоянию
    await message.answer (f'Хотите отправить это сообщение ВСЕМ пользователям?', reply_markup=keyboard_build_query)


@dp.message_handler(state=Form.waiting_for_message, content_types=types.ContentTypes.TEXT)
async def process_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(
        "Теперь отправьте изображение, если хотите его добавить, или введите /confirm для подтверждения отправки.")


@dp.message_handler(state=Form.waiting_for_message, content_types=types.ContentTypes.PHOTO)
async def process_photo(message: types.Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)
    await message.answer("Изображение добавлено. Для подтверждения отправьте /confirm.")

@dp.callback_query_handler(lambda callback: callback.data in ["Confirm", "StopMsg"], state=Form.waiting_for_confirmation)
async def process_confirmation(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    text_msg = user_data.get('text', '')
    photo_id = user_data.get('photo')
    curr_data = callback.data

    if curr_data == "Confirm":
        # Отправляем сообщение всем пользователям из списка user_ids
        db = DataBase()
        res = db.get_all_users_from_database(callback.from_user.id)
        users_count = len(res)
        if not isinstance(res, list):
            await callback.answer(f'Не удалось отправить сообщение {res}')
        for data in res:
            tg_id = data[0]
            username = data[1]
            try:
                if photo_id:
                    await bot.send_photo(tg_id, photo=photo_id, caption=text_msg)
                else:
                    await bot.send_message(tg_id, text_msg)
            except Exception as e:
                users_count -= 1
                await bot.send_message(callback.from_user.id, f'Could not send message: {tg_id}:{username}: {e}')

        await callback.answer(f'Сообщение было успешно отправлено {users_count} пользователям!')
        await bot.send_message(callback.from_user.id, f'Сообщение было успешно отправлено {users_count} пользователям!')
    else:
        await bot.send_message(callback.from_user.id, f'Отправка сообщения отменена')
        await callback.answer("Отправка сообщения отменена")
    await state.finish()  # Завершение состояния


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(commands_start, commands=[
        'start'], state='*')  # /start
    dp.register_message_handler(commands_help, commands=[
        'help'], state='*')  # /help
    dp.register_message_handler(commands_rasselenie, commands=[
        'resettlement_dep'], state='*')  # /resettlement_dep
    dp.register_message_handler(
        commands_wash_clothes, commands=['wash_clothes'], state='*')  # /wash_clothes
    dp.register_message_handler(commands_feedback, commands=[
        'feedback'], state='*')
    dp.register_message_handler(commands_get_information, commands=[
        'information'], state='*')
    dp.register_message_handler(
        commands_recycle_dsl, commands=['recycle_dsl'], state='*')  # /recycle_dsl
    dp.register_message_handler(
        commands_gym_dsl, commands=['gym_dsl'], state='*')  # /gym_dsl
    dp.register_message_handler(food_command, commands=['food', 'shop', 'admin_ds'], state='*')

    dp.register_message_handler(commands_horo_help, commands=['horo_help'], state='*')  # /horo_help
    dp.register_message_handler(set_time_horo, commands=['horo_time'], state='*')  # /horo_time
    dp.register_message_handler(subscribe_horo, commands=['horo_sub'], state='*')  # /horo_sub
    dp.register_message_handler(unsubscribe_horo, commands=['horo_unsub'], state='*')  # /horo_unsub

    dp.register_message_handler(help_admin, commands=['help_admin'], state='*')  # /help_admin
    dp.register_message_handler(set_admin_for_user, commands=['set_admin'], state='*')  # /set_admin
    dp.register_message_handler(notify_all_users, commands=['notify'], state='*')  # notify

    dp.register_message_handler(echo_error, state='*')
