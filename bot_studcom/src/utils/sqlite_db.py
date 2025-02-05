import sqlite3 as sq
import config
import logging


class Fields:
    telegram_id = 'telegram_id'
    telegram_name = 'telegram_name'
    is_admin = 'is_admin'
    building = 'building'


class DataBase():
    # is_admin 0 means that user is not admin otherwise 1 is_admin

    def __init__(self, filename=config.FileLocation.database):
        self.filename = filename
        with sq.connect(filename) as con:
            cursor = con.cursor()
            cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS users(
            {Fields.telegram_id} INTEGER PRIMARY KEY, 
            {Fields.telegram_name} TEXT,
            {Fields.is_admin} INTEGER DEFAULT 0,
            {Fields.building} TEXT
            )
            ''')
        logging.log(level=logging.INFO, msg=f'Successfully Connected to {filename}')

    def is_user_exists_in_database(self, cursor, tg_id: int) -> bool:
        cursor.execute(f'SELECT * FROM users WHERE {Fields.telegram_id} = ?', (tg_id,))
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False

    def is_user_exists(self, cursor, username: str) -> bool:
        cursor.execute(f'SELECT * FROM users WHERE {Fields.telegram_name} = ? ', (username,))
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False

    def is_user_admin(self, cursor, tg_id: int) -> bool:
        cursor.execute(f'SELECT * FROM users WHERE {Fields.telegram_id} = ? and {Fields.is_admin} = 1', (tg_id,))
        data = cursor.fetchone()
        if data:
            return True
        else:
            return False

    def register_user_in_database_if_needed(self, tg_id: int, username: str):
        with sq.connect(self.filename) as con:
            cursor = con.cursor()
            if self.is_user_exists_in_database(cursor, tg_id):
                return
            cursor.execute(f'''
            INSERT INTO users ({Fields.telegram_id}, {Fields.telegram_name}) VALUES (?, ?)
            ''', (tg_id, username)
                           )

    def update_user_building(self, tg_id: int, building: str):
        with sq.connect(self.filename) as con:
            cursor = con.cursor()
            if not self.is_user_exists_in_database(cursor, tg_id):
                return
            cursor.execute(f'''
            UPDATE users SET {Fields.building} = ? WHERE {Fields.telegram_id} = ?
            ''',
                           (building, tg_id)
                           )

    def get_all_users_from_database(self, tg_id : int):
        with sq.connect(self.filename) as con:
            cursor = con.cursor()
            if not self.is_user_admin(cursor, tg_id):
                return f'{tg_id} not admin'
            cursor.execute(f'''
            SELECT {Fields.telegram_id}, {Fields.telegram_name} FROM users
            ''')
            result = cursor.fetchall()
            return result

    def get_admins_tg_ids(self):
        with sq.connect(self.filename) as con:
            cursor = con.cursor()
            cursor.execute(f'''
            SELECT {Fields.telegram_id} FROM users where {Fields.is_admin} = 1
            ''')
            lst = []
            for elem in cursor.fetchall():
                lst.append(elem[0])
            return lst


    def set_admin_for_user(self, requester_td_id: int, username: str, is_admin: int):
        with sq.connect(self.filename) as con:
            cursor = con.cursor()
            if not self.is_user_admin(cursor, requester_td_id):
                return f'User {requester_td_id} is not Allowed to add admins'
            if not self.is_user_exists(cursor, username):
                return f'Username {username} does not exists in database'
            cursor.execute(f'''
            UPDATE users SET {Fields.is_admin} = ? WHERE {Fields.telegram_name} = ?
            ''', (is_admin, username))
            return f'OK. is_admin: {is_admin}'
