from __future__ import print_function
from operator import attrgetter
from typing import NamedTuple
import time

from datetime import datetime
from httplib2 import Http
import requests

from init_env import *
from db_requests import write_to_database


from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



class OrdersInfo(NamedTuple):
    id: int
    order_id: int
    price_usd: int
    price_rub: int
    delivery_date: tuple


def get_usd_currency()-> int:
    resp = requests.get(f'{CURRCONV_API}{CURRCONV_API_KEY}').json()
    return int(resp['USD_RUB'])


def get_service_account():
    creds_json = "speedy-aurora_test-account-3.json"

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, SCOPES).authorize(Http())
    return build('sheets', 'v4', http=creds_service)


def get_spreadsheets()-> list:
    resp = get_service_account().spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    usd_rub = get_usd_currency()
    order_list = []
    for order in resp['values'][1:]:
        try:
            data = OrdersInfo(id=order[0],
                            order_id=order[1], 
                            price_usd=order[2], 
                            price_rub=str(int(order[2])*usd_rub), 
                            delivery_date=attrgetter(*('year', 'month', 'day'))((datetime.strptime(order[3], '%d.%m.%Y').date())))
        
            order_list.append(data)
        except:
            pass
    return order_list


def run():
    while True:
        #conn = connect_to_db()
        write_to_database(DB_TABLE, get_spreadsheets())
        time.sleep(TIMESTAMP)


if __name__ == '__main__':
    run()