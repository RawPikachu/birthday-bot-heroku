import psycopg2
import db.QUERIES as queries
from db.birthday import Birthday
from db.world import World
import os


def __create_connection():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(
        DATABASE_URL,
        sslmode='require'
    )
    return conn


def create_birthday_tables():
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.create_birthday_table)
    conn.commit()
    cursor.close()
    conn.close()


def drop_birthday_tables():
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.delete_birthday_table)
    conn.commit()
    cursor.close()
    conn.close()


def create_birthday(user_id, day, month, year):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.create_birthday, (user_id, day, month, year, month, day, year, user_id))
    conn.commit()
    cursor.close()
    conn.close()


def get_birthday_all():
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.get_birthday_all)
    rows = cursor.fetchall()
    birthdays = []
    for row in rows:
        birthdays.append(Birthday(user_id=row[0], day=row[1], month=row[2], year=row[3]))
    cursor.close()
    conn.close()
    return birthdays


def get_birthday_one(user_id):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.get_birthday_one, (user_id,))
    birthday_data = cursor.fetchone()
    result = None
    if birthday_data:
        result = Birthday(birthday_data[0], birthday_data[1], birthday_data[2], birthday_data[3])
    cursor.close()
    conn.close()
    return result


def update_birthday(user_id, day, month, year):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.update_birthday, (month, day, year, user_id))
    conn.commit()
    cursor.close()
    conn.close()


def delete_birthday(user_id):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.delete_birthday, (user_id,))
    conn.commit()
    cursor.close()
    conn.close()

def create_server_list_tables():
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.create_server_list_table)
    conn.commit()
    cursor.close()
    conn.close()


def drop_server_list_tables():
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.delete_server_list_table)
    conn.commit()
    cursor.close()
    conn.close()


def create_server_list(name, total_players, timestamp, min30_chest_count=None, chest_count=None, last_chest_count=None):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.create_server_list, (name, total_players, timestamp, min30_chest_count, chest_count, last_chest_count))
    conn.commit()
    cursor.close()
    conn.close()


def get_server_list_all():
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.get_server_list_all)
    rows = cursor.fetchall()
    server_list = []
    for row in rows:
        server_list.append(World(name=row[0], total_players=row[1], timestamp=row[2], uptime=row[3], min30_chest_count=row[4], chest_count=row[5], last_chest_count=row[6]))
    cursor.close()
    conn.close()
    return server_list


def get_server_list_one(name):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.get_server_list_one, (name,))
    server_list_data = cursor.fetchone()
    result = None
    if server_list_data:
        result = World(server_list_data[0], server_list_data[1], server_list_data[2], server_list_data[3])
    cursor.close()
    conn.close()
    return result


def update_server_list(name, total_players, timestamp, uptime="", min30_chest_count=None, chest_count=None, last_chest_count=None):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.update_server_list, (name, total_players, timestamp, uptime, min30_chest_count, chest_count, last_chest_count))
    conn.commit()
    cursor.close()
    conn.close()


def delete_server_list(name):
    conn = __create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.delete_server_list, (name,))
    conn.commit()
    cursor.close()
    conn.close()