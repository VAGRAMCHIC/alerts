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


CURRCONV_API = 'https://free.currconv.com/api/v7/convert?q=USD_RUB&compact=ultra&apiKey='
CURRCONV_API_KEY = get_env_variable('CURRCONV_API_KEY')

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = get_env_variable('SPREADSHEET_ID')
RANGE_NAME = get_env_variable('RANGE_NAME')
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


DB_BOT_TABLE=get_env_variable('DB_BOT_TABLE')
TG_API_TOKEN=get_env_variable('TG_API_TOKEN')
TG_BROADCAST_DELAY=int(get_env_variable('TG_BROADCAST_DELAY'))

TIMESTAMP=int(get_env_variable('TIMESTAMP'))

DB_TABLE=get_env_variable('DB_TABLE')
DATABASE = {
    'host': 'localhost',
    'port': '5432',
    'user': get_env_variable('DB_USER'),
    'password': get_env_variable('DB_USER_PASS'),
    'database': get_env_variable('DATABASE')
}