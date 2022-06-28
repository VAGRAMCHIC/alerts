'''Да. Думаю код ниже - такое себе зрелище'''

import logging

import psycopg2
from psycopg2 import Date
from datetime import datetime

from init_env import *


#Так как записывать в базу данных особо нечего, было принято решение свалить основной функционал записи в одну функцию
def write_to_database(data):
    session = psycopg2.connect(**DATABASE)
    cursor = session.cursor()

    order_ids = []
    try:
        for order in data:
            print(order)
            order_ids.append(order[0])
            cursor.execute(f'INSERT INTO {DB_TABLE} (id, id_order, price_usd, price_rub, delivery_date, is_notified) \
                            values ({order[0]}, {order[1]}, {order[2]}, {order[3]}, {Date(order[4][0],order[4][1], order[4][2])}, {False}) \
                            ON CONFLICT (id) DO NOTHING')
        cursor.execute(f'DELETE FROM {DB_TABLE} WHERE id NOT IN {tuple(order_ids)}')
        logging.info(f'data write succses')
    except psycopg2.Error as e:
        logging.error(f'incorrect dataset {e}')
        pass
      
    session.commit()
    cursor.close()
    session.close()

def read_from_database(date: None|datetime):
    session = psycopg2.connect(**DATABASE)
    cursor = session.cursor()
    if date is None:
        cursor.execute(f'SELECT * FROM {DB_TABLE}')
    else:
        cursor.execute(f'SELECT * FROM {DB_TABLE} WHERE delivery_date < {Date(date.year, date.month ,date.day)} AND is_notified = {False}')
    data = cursor.fetchall()
    
    cursor.close()
    session.close() 
    return data


# добавляем или удаляем рользователей
def manage_tg_users(action:bool, id: int):
    session = psycopg2.connect(**DATABASE)
    cursor = session.cursor()
    if action == True:
        cursor.execute(f'INSERT INTO {DB_BOT_TABLE} (id) values ({id}) ON CONFLICT (id) DO NOTHING')
    else:
        cursor.execute(f'DELETE FROM {DB_BOT_TABLE} where id = {id}')
    session.commit()
    cursor.close()
    session.close()


# В задании говорилось, что нужно передать данные в БД в исходном виде, но также следовало написать функционал для Telegram бота
def mark_as_notified(order_id):
    session = psycopg2.connect(**DATABASE)
    cursor = session.cursor()

    cursor.execute(f'UPDATE {DB_TABLE} SET is_notified = {True} WHERE id_order = {order_id}')
    session.commit()
    cursor.close()
    session.close() 


# получаем список подписчиков
def get_users():
    session = psycopg2.connect(**DATABASE)
    cursor = session.cursor()
    cursor.execute(f'SELECT * FROM {DB_BOT_TABLE}')

    data = cursor.fetchall()[0]

    cursor.close()
    session.close() 
    return data