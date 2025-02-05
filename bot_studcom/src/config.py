from os.path import join

# В кавычки нужно ввести токен из BotFather
TOKEN = '6618766493:AAExSHuMwIt126mg4F4mKUuiahcnOEwG32Y'


# TOKEN = "5713033359:AAEBBgn-55ZDfGVEgLqMTsUmsA3HAjwp5ko"

# Пути к папкам и файлам:

class FileLocation:
    data_dir = '../data/'
    html_dir = data_dir + 'html/'
    pics = data_dir + 'pics/'
    json_dir = data_dir + 'json/'
    sqlite_dir = data_dir + 'sqlite_db/'

    cmd_help = join(html_dir, 'cmd_help.html')
    cmd_comenda_info = join(html_dir, 'cmd_comenda_info.html')
    cmd_check_rooms_time = join(html_dir, 'cmd_check_rooms_time.html')
    cmd_my_starosta = join(html_dir, 'cmd_my_starosta.html')
    cmd_rasselenie_info = join(html_dir, 'cmd_rasselenie_info.html')
    cmd_horo_help = join(html_dir, 'cmd_horo_help.html')
    admin_help = join(html_dir, 'admin_help.html')

    time_json = json_dir + 'time.json'
    subsciptions_json = json_dir + 'subscriptions.json'

    database = sqlite_dir + 'user_database.sqlite'