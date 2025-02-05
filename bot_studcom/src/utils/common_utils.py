from utils.create_bot import dp, bot

import datetime
import json
import asyncio
import random
import config
import os
import requests
from bs4 import BeautifulSoup


async def subs_notify(subs, text, keyboard=None, me=None):
    fails = []
    for chat_id in subs:
        if chat_id != me:
            ret = await bot.send_message(
                chat_id, text, parse_mode='HTML', reply_markup=keyboard)
            if not ret:
                fails.append(str(chat_id))
                if me:
                    await bot.send_message(me, '⚠️ Сообщение {} не доставилось'.format(
                        link('адресату', chat_id)), parse_mode='HTML')
    if len(fails) != 0:
        action_log('Notifying failed for: [{}]'.format(', '.join(fails)))


def get_subscription_status(user_id):
    try:
        with open(config.FileLocation.subsciptions_json, 'r') as file:
            subscriptions = json.load(file)
    except FileNotFoundError:
        subscriptions = {}
    if str(user_id) in subscriptions:
        return subscriptions[str(user_id)]['sub']
    else:
        return False


def set_subscription_status(user_id, status):
    try:
        with open(config.FileLocation.subsciptions_json, 'r') as file:
            subscriptions = json.load(file)
    except FileNotFoundError:
        subscriptions = {}
    subscriptions[str(user_id)]['sub'] = status
    with open(config.FileLocation.subsciptions_json, 'w') as file:
        json.dump(subscriptions, file)


def get_subscribed_users():
    try:
        with open(config.FileLocation.subsciptions_json, 'r') as file:
            subscriptions = json.load(file)
    except FileNotFoundError:
        subscriptions = {}
    res_list = []
    for user_id in subscriptions:
        if subscriptions[user_id]['sub'] == True:
            res_list.append(user_id)
    return res_list
    # return [int(user_id) for user_id, subscribed in subscriptions.items() if subscribed]


def get_user_sign(user_id):
    with open(config.FileLocation.subsciptions_json, 'r') as file:
        subscriptions = json.load(file)
    return subscriptions[str(user_id)]['sign']


def get_user_time():
    try:
        with open(config.FileLocation.time_json, 'r') as file:
            time_res = json.load(file)
    except FileNotFoundError:
        time_res = {}
    return time_res['hour'], time_res['minutes']


async def send_daily_message(user_id):
    while True:
        if not get_subscription_status(user_id):
            break
        user_sign = get_user_sign(user_id)
        now = datetime.datetime.now()
        expected_hour, expected_minutes = get_user_time()
        if int(now.hour) == int(expected_hour) and int(now.minute) == int(expected_minutes):
            img, text = build_message(user_sign)
            await bot.send_photo(user_id, photo=img, caption=text, parse_mode='MarkdownV2')
            print("sended: " + str(user_id))
            await bot.send_message(575238020, f"Отправил доброе утро: {user_id}")
        await asyncio.sleep(50)


def sign_for_gui(sign):
    if sign == 'virgo':
        return '♍'
    if sign == 'aquarius':
        return '♒'
    if sign == 'pisces':
        return '♓'
    if sign == 'aries':
        return '  '
    if sign == 'taurus':
        return '  '
    return ""


def build_str_for_markdown(str_change):
    str_change = str_change.replace('.', '\.')
    str_change = str_change.replace('-', '\-')
    str_change = str_change.replace('!', '\!')
    return str_change


def build_message(user_sign):
    text_list = [
        '🇺🇸🇺🇸 Good morning 🇺🇸🇺🇸',
        '🇷🇸🇷🇸 Добро јутро 🇷🇸🇷🇸',
        '🇫🇷🇫🇷 Bonjour 🇫🇷🇫🇷',
        '🇮🇹🇮🇹 Buongiorno 🇮🇹🇮🇹',
        '🇫🇮🇫🇮 Huomenta 🇫🇮🇫🇮',
        '🇸🇪🇸🇪 God morgon 🇸🇪🇸🇪',
        '🇩🇪🇩🇪 Guten Morgen 🇩🇪🇩🇪',
        '🇬🇷🇬🇷 Καλημέρα 🇬🇷🇬🇷'
    ]

    text_ind = random.randint(0, len(text_list) - 1)
    text = text_list[text_ind]

    files = os.listdir(config.FileLocation.pics)
    selected_file = random.randint(0, len(files) - 1)
    pic_path = config.FileLocation.pics + files[selected_file]
    img = open(pic_path, 'rb')

    url = 'https://horo.mail.ru/prediction/' + user_sign + '/today/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        horoscope = soup.find('div', class_='article__item article__item_alignment_left article__item_html').text
        horoscope = build_str_for_markdown(horoscope)
        date_now = build_str_for_markdown(str(datetime.datetime.now()))
        text = text + '\n' + 'Гороскоп на сегодня' + sign_for_gui(
            user_sign) + '\n' + '|| ' + horoscope + ' ||' + '\n' + '\[' + date_now + '\]'
    return img, text
