import base64
import json

from envparse import env
from gspread import Client, Spreadsheet, service_account_from_dict


##метод для получения подключения к гугл таблице, возвращает Client
def client_init() -> Client:

    ##получаем из env массив с данными для подключения к гугл таблице
    encoded_key = env.str("SERVICE_ACCOUNT")[2:-1]
    cred = json.loads(base64.b64decode(encoded_key).decode("utf-8"))
    ## передаем его в метод подключения
    return service_account_from_dict(cred)


##Получение таблицы по ID таблицы
def get_table_by_id(client: Client, table_id) -> Spreadsheet:

    return client.open_by_key(table_id)


def extract_data_from_sheet(table: Spreadsheet, sheet_name: str) -> list[dict]:
    ##Извлекаем данные из указанного листа таблицы гугл и возвращаем список словарей.
    worksheet = table.worksheet(sheet_name)
    rows = worksheet.get_all_records()
    return rows
