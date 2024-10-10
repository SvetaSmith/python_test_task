import requests
from envparse import env



ApiKey = env.str("API_KEY")

HEADERS = {"Authorization": "ApiKey " + ApiKey}
HEADERS_JSON = {
    "Authorization": "ApiKey Jiuk4dvstHZ2BN",
    'Content-Type"': "application/json",
}
URL_GAME = "https://eu-central-1.api.gridly.com/v1/views/6y1zq93yb37py/records"
URL_STATIC = "https://eu-central-1.api.gridly.com/v1/views/n74lqytbjq2zl/records"


##получить данные таблицы Static Texts из гридли
def get_grid_static() -> list[dict]:
    # GET запрос с заголовком аутентификатором по адресу нужного вью
    response = requests.get(URL_STATIC, headers=HEADERS)
    return response.json()


##получить данные таблицы Game Text из гридли
def get_grid_game() -> list[dict]:
    # GET запрос с заголовком аутентификатором
    # по адресу нужного вью
    response = requests.get(URL_GAME, headers=HEADERS)
    return response.json()


##отправить запрос на добавление записей в гридли -
# выбор нужного вью это выбор адреса
def add_data(URL: str, data: list[dict]) -> bool:
    response = requests.post(URL, headers=HEADERS_JSON, json=data)
    if response:
        return True
    else:
        print("An error has occurred.", response.text)
        return False


## отправить запрос на добавление записей в таблицу Static Texts
def add_data_static(data: list[dict]) -> bool:
    return add_data(URL_STATIC, data)


## отправить запрос на добавление записей в таблицу Game Text
def add_data_game(data: list[dict]) -> bool:
    return add_data(URL_GAME, data)


##отправить запрос на обновление записей в гридли -
#  выбор нужного вью это выбор адреса
def update_data(URL: str, data: list[dict]) -> bool:
    response = requests.patch(URL, headers=HEADERS_JSON, json=data)

    if response:
        return True
    else:
        print("An error has occurred.", response.text)
        return False


## отправить запрос на обновление записей в таблицу Static Texts
def update_data_statis(data: list[dict]) -> bool:
    return update_data(URL_STATIC, data)


## отправить запрос на обновление записей в таблицу Game Text
def update_data_game(data: list[dict]) -> bool:
    return update_data(URL_GAME, data)
