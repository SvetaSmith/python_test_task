import gridly
import gtask

from envparse import env
from gspread import Spreadsheet


def main():

    table_id_my = env.str("TABLE_ID_MY")
    client = gtask.client_init()
    table = gtask.get_table_by_id(client, table_id_my)
    sync_game(table)
    sync_static(table)


##синхронизация данных таблицы Static Texts из гугл в гридли:
# новые записи вставляем, старые - обновляем, удаленные - пропускаем
def sync_static(table: Spreadsheet) -> bool:
    ##данные из гугл
    data_google_static = gtask.extract_data_from_sheet(table, "Static Texts")

    ##данные из gridly
    data_gridly_static = gridly.get_grid_static()

    # сравнение данных из источника - гугл и получателя - гридли
    # и формирование списков на добавление (новые RECORD_ID)
    #  и изменение (уже есть такие RECORD_ID, но изменились данные)
    # для таблицы Static Texts

    dif_update, dif_add = prepare_list_for_work(
        get_content_table_google_hash(data_google_static),
        get_content_table_gridly_hash(data_gridly_static),
    )

    ##если массивы не пусты то переформатируем записи в формат
    #  для гридли, собираем и отправляем запрос
    if len(dif_update) > 0:
        dif_update = make_data_for_request(dif_update)
        make_request_update_statis(dif_update)
        print("Обновлено", len(dif_update), "записей в Static Texts")
    else:
        print("Нет данных для обновления в Static Texts")

    if len(dif_add) > 0:
        dif_add = make_data_for_request(dif_add)
        make_request_add_statis(dif_add)
        print("Добавлено", len(dif_add), "записей в Static Texts")
    else:
        print("Нет данных для добавления в Static Texts")


##синхронизация данных таблицы Game Text из гугл в гридли:
# новые записи вставляем, старые - обновляем, удаланные - пропускаем
def sync_game(table: Spreadsheet) -> bool:
    ##данные из гугл
    data_google_game = gtask.extract_data_from_sheet(table, "Game Text")

    ##данные из gridly
    data_gridly_game = gridly.get_grid_game()

    # сравнение данных из источника - гугл и получателя - гридли
    # и формирование списков на добавление (новые RECORD_ID)
    #  и изменение (уже есть такие RECORD_ID, но изменились данные)
    # для таблицы Game Text

    dif_update, dif_add = prepare_list_for_work(
        get_content_table_google_hash(data_google_game),
        get_content_table_gridly_hash(data_gridly_game),
    )

    ##если массивы не пусты то переформатируем записи в формат
    #  для гридли, собираем и отправляем запрос
    if len(dif_update) > 0:
        dif_update = make_data_for_request(dif_update)
        make_request_update_game(dif_update)
        print("Обновлено", len(dif_update), "записей в Game Text")
    else:
        print("Нет данных для обновления в Game Text")

    if len(dif_add) > 0:
        dif_add = make_data_for_request(dif_add)
        make_request_add_game(dif_add)
        print("Добавлено", len(dif_add), "записей в Game Text")
    else:
        print("Нет данных для добавления в Game Text")


##добавляем в словарь пару hash, {hash,  хэш от полей со значениями},
# что бы не проверять каждое поле со значениями отдельно, а вставить всю строку
def get_content_table_google_hash(data: list[dict]) -> list[dict]:

    for i in range(len(data)):
        data_row = data[i]
        data_row["hash"] = hash(
            str(data_row["Character"])
            + str(data_row["Russian"])
            + str(data_row["English (United States)"])
            + str(data_row["Character limit"])
            + str(data_row["Version"])
            + str(data_row["NarrativeComment"])
        )

    return data


## переформатируем данные под более удобный вид,
# добавляем в словарь пару {hash,  хэш от полей со значениями},
# что бы не проверять каждое поле со значениями отдельно, а вставить всю строку
def get_content_table_gridly_hash(data: list[dict]) -> list[dict]:
    content_table_gridly = []

    for i in range(len(data)):
        data_row = data[i]
        content_table_gridly_row = {}

        content_table_gridly_row["Record ID"] = data_row["id"]
        content_table_gridly_row["Character"] = data_row["cells"][0]["value"]
        content_table_gridly_row["Russian"] = data_row["cells"][1]["value"]
        content_table_gridly_row["English (United States)"] = data_row["cells"][2][
            "value"
        ]
        content_table_gridly_row["Character limit"] = data_row["cells"][3]["value"]
        content_table_gridly_row["Version"] = data_row["cells"][4]["value"]
        content_table_gridly_row["NarrativeComment"] = data_row["cells"][5]["value"]

        content_table_gridly_row["hash"] = hash(
            str(content_table_gridly_row["Character"])
            + str(content_table_gridly_row["Russian"])
            + str(content_table_gridly_row["English (United States)"])
            + str(content_table_gridly_row["Character limit"])
            + str(content_table_gridly_row["Version"])
            + str(content_table_gridly_row["NarrativeComment"])
        )

        content_table_gridly.append(content_table_gridly_row)

    return content_table_gridly


## формируем список Record ID на обновление  dif_update
# и вставку dif_add, отделяем записи по новым Record ID
# и по изменению хэша
def prepare_list_for_work(
    data_source_hash: list[dict], data_storage_hash: list[dict]
) -> list[dict]:

    dif_update = []
    dif_add = []

    for data_source_hash_row in data_source_hash:
        rec_id = data_source_hash_row["Record ID"]
        hash_val = data_source_hash_row["hash"]
        flag = 0
        for data_storage_hash_row in data_storage_hash:
            if rec_id == data_storage_hash_row["Record ID"]:
                flag = 1
                if hash_val != data_storage_hash_row["hash"]:
                    dif_update.append(data_source_hash_row)
        if flag == 0:
            dif_add.append(data_source_hash_row)

    return dif_update, dif_add


####  сформировать данные запроса на апдейт и вставку в гридли
def make_data_for_request(data: list[dict]) -> list[dict]:
    list = []
    for data_row in data:
        list_cells = []
        list_cells = [
            {"columnId": "column1", "value": data_row["Character"]},
            {
                "columnId": "column2",
                "value": data_row["Russian"],
            },
            {
                "columnId": "column3",
                "sourceStatus": "readyForTranslation",
                "value": data_row["English (United States)"],
            },
            {
                "columnId": "column4",
                "dependencyStatus": "upToDate",
                "value": str(data_row["Character limit"]),
            },
            {"columnId": "column5", "value": str(data_row["Version"])},
            {"columnId": "column6", "value": data_row["NarrativeComment"]},
        ]
        list.append({"id": data_row["Record ID"], "cells": list_cells})

    return list


## отправить запрос в гридли на обновление данных statis
def make_request_update_statis(data: list[dict]) -> bool:

    result = gridly.update_data_statis(data)
    return result


## отправить запрос в гридли на добавление данных statis
def make_request_add_statis(data: list[dict]) -> bool:

    result = gridly.add_data_static(data)
    return result


## отправить запрос в гридли на обновление данных game
def make_request_update_game(data: list[dict]) -> bool:

    result = gridly.update_data_game(data)
    return result


## отправить запрос в гридли на добавление данных game
def make_request_add_game(data: list[dict]) -> bool:

    result = gridly.add_data_game(data)
    return result


if __name__ == "__main__":
    main()
