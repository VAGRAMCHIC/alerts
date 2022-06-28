from __future__ import print_function
from operator import attrgetter
from xml.etree import ElementTree
import time


from datetime import datetime
from httplib2 import Http
import requests

from init_env import *
from db_requests import write_to_database


from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Курс доллара по ЦБ РФ
def get_cbrf_currency() -> float:
    resp = ElementTree.fromstring(requests.get('http://www.cbr.ru/scripts/XML_daily.asp').content)
    for valute in resp.findall('Valute'):
        if valute.find('CharCode').text == 'USD':
            return float(valute[4].text.replace(',', '.'))


# Авторизация через сервисный аккаунт
def get_service_account():
    creds_service = ServiceAccountCredentials.from_json_keyfile_name(CREDITS_JSON_FILE, SCOPES).authorize(Http())
    return build('sheets', 'v4', http=creds_service)


# Загрузка таблицы, если на момент загрузки таблица редактируется запись элемента пропускается
def get_spreadsheets()-> list:
    resp = get_service_account().spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range='Лист1!A:D').execute()
    usd_rub = get_cbrf_currency()
    order_list = []
    for order in resp['values'][1:]:
        try:
            data = (order[0], order[1], order[2], str(int(order[2])*usd_rub), 
                    attrgetter(*('year', 'month', 'day'))((datetime.strptime(order[3], '%d.%m.%Y').date())))        
            order_list.append(data)
        except:
            pass
    return order_list
    

if __name__ == '__main__':
    while True:
        try:
            write_to_database(get_spreadsheets())
            time.sleep(TIMESTAMP)

        except Exception as e:
            print(e)
            time.sleep(1)