import time

from modules.csv_reader import read_csv_one_line, read_csv_all
from modules.handlers import users_functions


# Показываем пост для админа
def get_multipost_text(user_id):
    index_market = users_functions.read_data1(user_id)
    description = users_functions.read_data2(user_id)
    status = users_functions.read_data3(user_id)

    category_index = str(index_market).split('_')[0]
    market_index = str(index_market).split('_')[1]

    market_name = users_functions.get_market_name(category_index=int(category_index),
                                                  market_index=int(market_index))
    cod = read_csv_one_line()
    if str(status) == 'premium':
        for_users = 'Только премиум'
    else:
        for_users = 'Для всех'
    text = f"<b>Компания:</b> {market_name}\n" \
           f"<b>Промокод:</b> <code>{cod}</code>\n\n" \
           f"{description}\n\n" \
           f"_________________________________\n" \
           f"<b>Тип:</b> multicod, <b>Для кого:</b> {for_users}"
    return text


# Показываем пост для админа
def get_post_text(user_id):
    index_market = users_functions.read_data1(user_id)
    description = users_functions.read_data2(user_id)
    cod = users_functions.read_data3(user_id)
    single_status = users_functions.read_data4(user_id)
    status = users_functions.read_data5(user_id)

    category_index = str(index_market).split('_')[0]
    market_index = str(index_market).split('_')[1]

    market_name = users_functions.get_market_name(category_index=int(category_index),
                                                  market_index=int(market_index))
    if str(single_status) == 'single':
        post_text = 'Одноразовый'
    else:
        post_text = 'Многоразовый'

    if str(status) == 'premium':
        for_users = 'Только премиум'
    else:
        for_users = 'Для всех'

    text = f"<b>Компания:</b> {market_name}\n" \
           f"<b>Промокод:</b> <code>{cod}</code>\n\n" \
           f"{description}\n\n" \
           f"_________________________________\n" \
           f"<b>Тип:</b> {post_text}, <b>Для кого:</b> {for_users}"
    return text


# Показываем пост для пользователя
def get_post_text_user(cod: str, description: str, market_name: str):

    text = f"<b>Компания:</b> {market_name}\n" \
           f"<b>Промокод:</b> <code>{cod}</code>\n\n" \
           f"{description}"
    return text


# Сохраняем пост в базу данных
def save_post(user_id: int):
    index_market = users_functions.read_data1(user_id)
    description = users_functions.read_data2(user_id)
    cod = users_functions.read_data3(user_id)
    single_status = users_functions.read_data4(user_id)
    status = users_functions.read_data5(user_id)

    users_functions.save_post_category(index=index_market, cod=cod, description=description, type_time=status,
                                       type_users=single_status)


# Сохраняем мультипост в базу данных
def save_multipost(user_id: int):
    index_market = users_functions.read_data1(user_id)
    description = users_functions.read_data2(user_id)
    status = users_functions.read_data3(user_id)
    post_id = int(users_functions.get_lust_post_id(index_market)) + 1

    users_functions.save_post_category(index=index_market, cod=f'multi_{index_market}_{post_id}',
                                       description=description, type_time=status, type_users='multicod')
    users_functions.creat_multipost_cods(table_name=f'multi_{index_market}_{post_id}')
    time.sleep(0.25)
    cods = read_csv_all().split('|')
    for cod in cods:
        users_functions.save_multipost_cods(table_name=f'multi_{index_market}_{post_id}', cod=cod)

