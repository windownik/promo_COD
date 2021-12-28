import requests
from modules.dispatcher import constant

url = constant.server()


def create_tables():
    data = url + f'init/'
    response = requests.get(data)
    return response.json()


def update_user_data(tg_id: int, name: str):
    data = url + f'new_user/{tg_id}/{name}/'
    response = requests.get(data)
    return response.json()


# Создаем запрос на нового админа
def create_admin(tg_id: int):
    data = url + f'new_admin/{tg_id}/'
    response = requests.get(data)
    return response.json()


# Создаем запрос на нового админа
def ban_user(tg_id: int):
    data = url + f'ban_user/{tg_id}/'
    response = requests.get(data)
    return response.json()


# Записываем телефонный номер в премиум
def save_phone(tg_id: int, phone: str):
    data = url + f'save_phone/{tg_id}/{phone}/'
    response = requests.get(data)
    return response.json()


# Удаляем админа
def delete_admin(tg_id: int):
    data = url + f'delete_admin/{tg_id}/'
    response = requests.get(data)
    return response.json()


# Проверяем статус пользователя
def is_admin(tg_id: int):
    data = url + f'is_admin_user/{tg_id}/'
    response = requests.get(data)
    return response.json()['admin']


# Проверяем premium статус пользователя
def is_premium(tg_id: int):
    data = url + f'is_user_premium/{tg_id}/'
    response = requests.get(data)
    return response.json()['premium']


# Получаем категории
def get_category():
    data = url + f'categorys/'
    response = requests.get(data)
    return response.json()


# Получаем под категории
def get_sub_category(index: int):
    data = url + f'sub_categorys/{index}/'
    response = requests.get(data)
    return response.json()


def create_category(name: str):
    data = url + f'categorys/create/{name}/'
    response = requests.get(data)

    return response.json()


def delete_category(index: str):
    data = url + f'categorys/delete/{index}/'
    response = requests.get(data)

    return response.json()


def get_name(index: int):
    data = url + f'category/{index}/'
    response = requests.get(data)

    return response.json()


def get_market_name(category_index: int, market_index: int):
    data = url + f'category/market_name/{category_index}/{market_index}/'
    response = requests.get(data)

    return response.json()['name']


# Сохраняем временную информацию 1
def save_data1(tg_id: int, data):
    data = url + f'data1/{tg_id}/{data}/'
    response = requests.get(data)

    return response.json()


# Сохраняем временную информацию 2
def save_data2(tg_id: int, data):
    data = url + f'data2/{tg_id}/{data}/'
    response = requests.get(data)

    return response.json()


# Сохраняем временную информацию 3
def save_data3(tg_id: int, data):
    data = url + f'data3/{tg_id}/{data}/'
    response = requests.get(data)

    return response.json()


# Сохраняем временную информацию 4
def save_data4(tg_id: int, data):
    data = url + f'data4/{tg_id}/{data}/'
    response = requests.get(data)

    return response.json()


# Сохраняем временную информацию 5
def save_data5(tg_id: int, data):
    data = url + f'data5/{tg_id}/{data}/'
    response = requests.get(data)

    return response.json()


# Читаем временную информацию 1
def read_data1(tg_id: int):
    data = url + f'data1/read/{tg_id}/'
    response = requests.get(data)
    return response.json()['data_1']


# Читаем временную информацию 2
def read_data2(tg_id: int):
    data = url + f'data2/read/{tg_id}/'
    response = requests.get(data)
    return response.json()['data_2']


# Читаем временную информацию 3
def read_data3(tg_id: int):
    data = url + f'data3/read/{tg_id}/'
    response = requests.get(data)
    return response.json()['data_3']


# Читаем временную информацию 4
def read_data4(tg_id: int):
    data = url + f'data4/read/{tg_id}/'
    response = requests.get(data)
    return response.json()['data_4']


# Читаем временную информацию 5
def read_data5(tg_id: int):
    data = url + f'data5/read/{tg_id}/'
    response = requests.get(data)
    return response.json()['data_5']


# Меняем имя категории
def correct_name(index: int, name):
    data = url + f'category_correct/{index}/{name}/'
    requests.get(data)


# Меняем имя под категории
def correct_market_name(category_index: int, market_index: int, name):
    data = url + f'category/rename_market/{category_index}/{market_index}/{name}/'
    requests.get(data)


# Создаем магазин (суб категорию)
def create_sub_category(name: str, index: int):
    data = url + f'create_sub_category/{name}/{index}/'
    response = requests.get(data)

    return response.json()


def delete_sub_category(category_index: int, market_index: int):
    data = url + f'category/delete_market/{category_index}/{market_index}/'
    response = requests.get(data)

    return response.json()


def save_post_category(index: str, cod: str, description: str, type_time: str, type_users: str):
    data = url + f'save_new_post/{index}/{cod}/{description}/{type_time}/{type_users}/'
    response = requests.get(data)

    return response.json()


def get_post(call_data: str, tg_id: int):
    data = url + f'get_post/{call_data}/{tg_id}/'
    response = requests.get(data)
    return response.json()


def get_10_post(category_index: str, market_index: str):
    data = url + f'get_10_posts_by_index/{category_index}/{market_index}/'
    response = requests.get(data)
    return response.json()


def get_premium_post(call_data: str, tg_id: int):
    data = url + f'get_premium_post/{call_data}/{tg_id}/'
    response = requests.get(data)
    return response.json()


def get_post_by_index(cod: str):
    data = url + f'get_post/by_index/{cod}/'
    response = requests.get(data)
    return response.json()


# Получаем id номер последнего предложения в базеданных
def get_lust_post_id(index: str):
    data = url + f'get_lust_post_id/{index}/'
    response = requests.get(data)
    return response.json()['number_posts']


def get_my_favorite_posts(tg_id: int):
    data = url + f'get_my_post/{tg_id}/'
    response = requests.get(data)

    return response.json()


def delete_my_post(tg_id: int, post_data: str):
    data = url + f'delete_my_post/{tg_id}/{post_data}/'
    response = requests.get(data)
    return response.json()


# Отправляем жалобу
def send_report(report_text: str, tg_id: int):
    data = url + f'send_report/{report_text}/{tg_id}/'
    response = requests.get(data)

    return response.json()


# Получаем категории
def get_moder_chat():
    data = url + f'moder_chat/get/'
    response = requests.get(data)
    return response.json()


def send_new_chat_id(chat_id: str):
    data = url + f'send_chat_id/{chat_id}/'
    response = requests.get(data)

    return response.json()


def find_user(text: str):
    data = url + f'find_user/{text}/'
    response = requests.get(data)

    return response.json()['find_user']


# Сохраняем все коды из файла в таблицу multicod
def creat_multipost_cods(table_name: str):
    data = url + f'creat_new_table/{table_name}/'
    response = requests.get(data)

    return response.json()


# Сохраняем все коды из файла в таблицу multicod
def save_multipost_cods(table_name: str, cod: str):
    data = url + f'save_multipost_cod/{table_name}/{cod}/'
    requests.get(data)


# Сохраняем все коды из файла в таблицу multicod
def search_post_by_cod(cod: str):
    data = url + f'search_post_by_cod/{cod}/'
    response = requests.get(data)

    return response.json()["post_inform"]


# Обновляем описание предложения
def update_post_description(cod: str, description: str):
    data = url + f'update_post_description/{cod}/{description}/'
    requests.get(data)


# Удаляем пост
def update_post_status(cod: str, status: str):
    data = url + f'update_post_status/{cod}/{status}/'
    requests.get(data)


# Получаем статистику
def get_users_statistic():
    data = url + f'get_users_statistic/'
    response = requests.get(data)
    return response.json()


# Получаем статистику
def get_bad_cod_statistic():
    data = url + f'get_bad_cod_statistic/'
    response = requests.get(data)
    return response.json()


# Получаем статистику
def get_top_categorys():
    data = url + f'get_top_categorys/'
    response = requests.get(data)
    return response.json()['favorite_category']
