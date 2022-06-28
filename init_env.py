

'''Загрузка переменных из .env файла в окружение и из него в данный
    модуль с последующим подключением к другим'''

from dotenv import load_dotenv
from pathlib import Path
import os


try:
    env_path = Path(os.getcwd())/'.env'
    if os.path.exists(env_path):
        load_dotenv(dotenv_path = env_path)
except Exception as e:
    exit()


def get_env_variable(env_var_name: str):
    if os.getenv(env_var_name):
        return os.getenv(env_var_name)


# Googlesheets api
SPREADSHEET_ID = get_env_variable('SPREADSHEET_ID')
RANGE_NAME = get_env_variable('RANGE_NAME')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDITS_JSON_FILE=get_env_variable('CREDITS_JSON_FILE')

# Telegram
DB_BOT_TABLE=get_env_variable('DB_BOT_TABLE')
TG_API_TOKEN=get_env_variable('TG_API_TOKEN')
TG_BROADCAST_DELAY=int(get_env_variable('TG_BROADCAST_DELAY'))


# Задержка между запросами к googlesheets
TIMESTAMP=int(get_env_variable('TIMESTAMP'))


#Данные БД
DB_TABLE=get_env_variable('DB_TABLE')
DATABASE = {
    'host': 'localhost',
    'port': '5432',
    'user': get_env_variable('DB_USER'),
    'password': get_env_variable('DB_USER_PASS'),
    'database': get_env_variable('DATABASE')
}