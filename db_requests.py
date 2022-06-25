import psycopg2
from psycopg2 import Date
from datetime import datetime

from requests import session

from init_env import *




def write_to_database(table:str, data):
    session = psycopg2.connect(**DATABASE)
    cursor = session.cursor()

    if table == DB_TABLE:
        order_ids = []
        for order in data:
            order_ids.append(order.order_id)
            cursor.execute(f'INSERT INTO {DB_TABLE} (id, id_order, price_usd, price_rub, delivery_date, is_notified) \
                            values ({order.id}, {order.order_id}, {order.price_usd}, {order.price_rub}, {Date(order.delivery_date[0],order.delivery_date[1], order.delivery_date[2])}, {False}) \
                            ON CONFLICT (id) DO NOTHING')
        cursor.execute(f'DELETE FROM {DB_TABLE} WHERE id_order NOT IN {tuple(order_ids)}')
    elif table == DB_BOT_TABLE:
        cursor.execute(f'INSERT INTO {DB_BOT_TABLE} (id) values ({data})')
    else:
        raise 'incorrect database table'
    session.commit()
    cursor.close()
    session.close()

def mark_as_notified(order_id):
    session = psycopg2.connect(**DATABASE)
    cursor = session.cursor()
    cursor.execute(f'UPDATE {DB_TABLE} SET is_notified = {True} WHERE id_order = {order_id}')
    session.commit()
    cursor.close()
    session.close() 

def read_from_database(date=None|datetime):
    session = psycopg2.connect(**DATABASE)
    cursor = session.cursor()
    if date is None:
        cursor.execute(f'SELECT * FROM {DB_TABLE}')
    else:
        cursor.execute(f'SELECT * FROM {DB_TABLE} WHERE delivery_date < {Date(date.year, date.month ,date.day)}')
    data = cursor.fetchall()
    
    cursor.close()
    session.close() 
    return data

def get_users():
    session = psycopg2.connect(**DATABASE)
    cursor = session.cursor()
    cursor.execute(f'SELECT * FROM {DB_BOT_TABLE}')

    data = cursor.fetchall()[0]

    cursor.close()
    session.close() 
    return data