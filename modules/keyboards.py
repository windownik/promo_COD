from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


send_contact = KeyboardButton(text=f'📞Поделится контактом', request_contact=True)

send_contact_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(send_contact)


def start_user_kb():
    get_cod = InlineKeyboardButton(text='🛍 Получить код', callback_data='get_cod')
    my_cod = InlineKeyboardButton(text='🛒 Мои промокоды', callback_data='my_cod')
    cod_for_u = InlineKeyboardButton(text='🔎📝 Специально для тебя!', callback_data='premium_cod_for_u')
    feed_back = InlineKeyboardButton(text='✏️ Обратная связь', callback_data='feed_back')
    start_kb = InlineKeyboardMarkup().add(get_cod, my_cod)
    start_kb.add(cod_for_u)
    start_kb.add(feed_back)
    return start_kb


def user_second_kb(cod_id=False):
    my_cod = InlineKeyboardButton(text='🛒 Мои промокоды', callback_data='my_cod')
    get_more_cod = InlineKeyboardButton(text='📝 Получить еще промокод!', callback_data='get_more_cod')
    if cod_id:
        bad_cod = InlineKeyboardButton(text='😢 Промокод не работает', callback_data=f'bad_cod{cod_id}')
    else:
        bad_cod = InlineKeyboardButton(text='😢 Промокод не работает', callback_data='bad_cod')
    start_kb = InlineKeyboardMarkup().add(my_cod)
    start_kb.add(get_more_cod)
    start_kb.add(bad_cod)
    return start_kb


def start_admin_kb():
    create_post = InlineKeyboardButton(text='📝 Создать пост', callback_data='create_post')
    my_bot = InlineKeyboardButton(text='✏️ Модерация', callback_data='my_bot')
    posts = InlineKeyboardButton(text='Посты', callback_data='posts')
    admins = InlineKeyboardButton(text='Админы', callback_data='admins')
    inform = InlineKeyboardButton(text='Статистика', callback_data='inform')
    as_user = InlineKeyboardButton(text='Зайти как user', callback_data='as_user')
    start_kb = InlineKeyboardMarkup().add(create_post)
    start_kb.add(my_bot)
    start_kb.add(posts, admins)
    start_kb.add(inform, as_user)
    return start_kb


def moderation_kb():
    category = InlineKeyboardButton(text='📝 Категории', callback_data='category')
    moder_chat = InlineKeyboardButton(text='🗯 Чат модерации', callback_data='moder_chat')
    back = InlineKeyboardButton(text='🔙 Назад', callback_data='back')

    start_kb = InlineKeyboardMarkup().add(category)
    start_kb.add(moder_chat)
    start_kb.add(back)
    return start_kb


# Клавиатура для категорий
def category_kb(category: dict = None):
    category_kb = InlineKeyboardMarkup()
    if category is None:
        pass
    else:
        for key in category.keys():
            btn = InlineKeyboardButton(text=category[key], callback_data=f'category_{key}')
            category_kb.add(btn)

    add_category = InlineKeyboardButton(text='➕ Добавить категорию.', callback_data='add_category')
    back = KeyboardButton(text='🔙 Назад', callback_data='category_back')

    category_kb.add(add_category)
    category_kb.add(back)
    return category_kb


# Клавиатура для под категорий
def podcategory_kb(index: int, category: dict = None):
    category_kb = InlineKeyboardMarkup()
    if category is None:
        pass
    else:
        for key in category.keys():
            btn = InlineKeyboardButton(text=category[key], callback_data=f'subcategory_{index}_{key}')
            category_kb.add(btn)

    add_category = InlineKeyboardButton(text='➕ Добавить подкатегорию.', callback_data=f'add_podcategory_{index}')
    correct_name = InlineKeyboardButton(text='✏️ Изменить название', callback_data=f'correct_name_{index}')
    delete_category = InlineKeyboardButton(text='❌ удалить эту категорию', callback_data=f'delete_category_{index}')
    back = KeyboardButton(text='🔙 Назад', callback_data=f'back_category')

    category_kb.add(add_category)
    category_kb.add(correct_name, delete_category)
    category_kb.add(back)
    return category_kb


# Клавиатура для под категорий
def confirm_kb(index):
    category_kb = InlineKeyboardMarkup()
    if index is None:
        confirm = InlineKeyboardButton(text='Да! Все верно!', callback_data=f'confirm')
        back = KeyboardButton(text='🔙 Назад', callback_data=f'back')
    else:
        confirm = InlineKeyboardButton(text='Да! Все верно!', callback_data=f'confirm_{index}')
        back = KeyboardButton(text='🔙 Назад', callback_data=f'backsub_{index}')

    category_kb.add(confirm, back)
    return category_kb


# Клавиатура для под категорий
def market_kb(category_index: int, market_index: int):
    category_kb = InlineKeyboardMarkup()

    correct_name = InlineKeyboardButton(text='✏️ Изменить название',
                                        callback_data=f'correct_name_{category_index}_{market_index}')
    delete_category = InlineKeyboardButton(text='❌ удалить этот магазин',
                                           callback_data=f'delete_market_{category_index}_{market_index}')
    back = KeyboardButton(text='🔙 Назад', callback_data=f'back_subc{category_index}')

    category_kb.add(correct_name)
    category_kb.add(delete_category)
    category_kb.add(back)
    return category_kb


# Клавиатура для под категорий для создания постов
def category_front_kb(category: dict = None):
    category_kb = InlineKeyboardMarkup()
    if category is None:
        pass
    else:
        for key in category.keys():
            btn = InlineKeyboardButton(text=category[key], callback_data=f'category_{key}')
            category_kb.add(btn)

    back = KeyboardButton(text='🔙 Назад', callback_data=f'back_category')

    category_kb.add(back)
    return category_kb


# Клавиатура для под категорий
def podcategory_front_kb(index: int, category: dict = None):
    category_kb = InlineKeyboardMarkup()
    if category is None:
        pass
    else:
        for key in category.keys():
            btn = InlineKeyboardButton(text=category[key], callback_data=f'subcategory_{index}_{key}')
            category_kb.add(btn)

    back = KeyboardButton(text='🔙 Назад', callback_data=f'back_category')

    category_kb.add(back)
    return category_kb


# Клавиатура для выбора типа отправки промокодов
def type_send_cod():
    send_cod_kb = InlineKeyboardMarkup()
    get_file = KeyboardButton(text='Файл', callback_data=f'get_file')
    get_text = KeyboardButton(text='Одиночный', callback_data=f'get_text')

    send_cod_kb.add(get_file)
    send_cod_kb.add(get_text)
    return send_cod_kb


# Клавиатура для выбора типа отправки промокодов
def post_type():
    send_cod_kb = InlineKeyboardMarkup()
    single = KeyboardButton(text='Одноразовый', callback_data=f'single')
    for_all = KeyboardButton(text='Многоразовый', callback_data=f'for_all')

    send_cod_kb.add(single)
    send_cod_kb.add(for_all)
    return send_cod_kb


# Клавиатура для выбора типа отправки промокодов
def post_user_type():
    send_cod_kb = InlineKeyboardMarkup()
    single = KeyboardButton(text='Для премиум', callback_data=f'premium')
    for_all = KeyboardButton(text='Для всех', callback_data=f'simple')

    send_cod_kb.add(single)
    send_cod_kb.add(for_all)
    return send_cod_kb


# Клавиатура для выбора типа отправки промокодов
def send_post_kb():
    send_cod_kb = InlineKeyboardMarkup()
    confirm = KeyboardButton(text='✔️Да! Все верно!', callback_data=f'confirm')
    back = KeyboardButton(text='🔙 Назад', callback_data=f'back')

    send_cod_kb.add(confirm)
    send_cod_kb.add(back)
    return send_cod_kb


# Клавиатура для выбора типа отправки промокодов
def my_posts_kb(last_post: int = 1, all_posts: int = 1, cod_id=False):
    send_posts_kb = InlineKeyboardMarkup()
    previous = KeyboardButton(text='⬅️ Назад', callback_data=f'previous_{last_post}')
    empty = KeyboardButton(text=f'{last_post}/{all_posts}', callback_data=f'empty')
    next = KeyboardButton(text='Далее ➡️', callback_data=f'next_{last_post}')
    del_post = KeyboardButton(text='🗑 Удалить', callback_data=f'delpost_{last_post}')
    if cod_id:
        bad_cod = InlineKeyboardButton(text='😢 Промокод не работает', callback_data=f'bad_cod{cod_id}')
    else:
        bad_cod = InlineKeyboardButton(text='😢 Промокод не работает', callback_data='bad_cod')
    go_to_main = KeyboardButton(text='🔝 На главную', callback_data=f'go_to_main')

    send_posts_kb.add(previous, empty, next)
    send_posts_kb.add(del_post)
    send_posts_kb.add(bad_cod)
    send_posts_kb.add(go_to_main)
    return send_posts_kb


def go_to_main():
    go_to_main_kb = InlineKeyboardMarkup()
    go_to_main = KeyboardButton(text='🔝 На главную', callback_data=f'go_to_main')
    go_to_main_kb.add(go_to_main)
    return go_to_main_kb


def feed_back():
    go_to_main_kb = InlineKeyboardMarkup()
    feed_back = KeyboardButton(text='✏️ Написать модератору', url='https://t.me/sovacode')
    go_to_main = KeyboardButton(text='🔝 На главную', callback_data=f'go_to_main')
    go_to_main_kb.add(feed_back)
    go_to_main_kb.add(go_to_main)
    return go_to_main_kb


# Клавиатура для категорий
def back_kb():
    category_kb = InlineKeyboardMarkup()
    back = KeyboardButton(text='🔙 Назад', callback_data='category_back')
    category_kb.add(back)
    return category_kb


# Клавиатура для работы с пользователями
def new_admin_kb(tg_id: int):
    category_kb = InlineKeyboardMarkup()
    ban_user = KeyboardButton(text='Заблокировать', callback_data=f'ban_user_{tg_id}')
    delete_admin = KeyboardButton(text='Сделать простым юзером', callback_data=f'delete_admin_{tg_id}')
    set_admin = KeyboardButton(text='Сделать админом', callback_data=f'set_admin_{tg_id}')
    back = KeyboardButton(text='🔙 Назад', callback_data='category_back')
    category_kb.add(delete_admin)
    category_kb.add(set_admin)
    category_kb.add(ban_user, back)
    return category_kb


# Клавиатура для работы админа с статистикой
def new_admin_stat():
    category_kb = InlineKeyboardMarkup()
    admin_stat = KeyboardButton(text='📝 Статистика постов', callback_data='posts_stat')
    users_stat = KeyboardButton(text='Статистика пользователей', callback_data='users_stat')
    back = KeyboardButton(text='🔙 Назад', callback_data='back')
    category_kb.add(admin_stat)
    category_kb.add(users_stat)
    category_kb.add(back)
    return category_kb


# Клавиатура для работы админа с статистикой
def stat_posts():
    stat_posts = InlineKeyboardMarkup()
    bad_cod = KeyboardButton(text='Количество брака', callback_data='bad_cod')
    top_category = KeyboardButton(text='Топ категорий', callback_data='top_category')
    # top_posts = KeyboardButton(text='Топ любимых магазинов', callback_data='top_market')
    back = KeyboardButton(text='🔙 Назад', callback_data='back')
    stat_posts.add(bad_cod)
    stat_posts.add(top_category)
    # stat_posts.add(top_posts)
    stat_posts.add(back)
    return stat_posts


# Клавиатура для работы админа с статистикой
def search_posts():
    start_posts = InlineKeyboardMarkup()
    posts_in_market = KeyboardButton(text='Поиск в недавних в магазинах', callback_data='posts_in_market')
    search_by_number = KeyboardButton(text='Поиск по номеру', callback_data='search_by_number')
    back = KeyboardButton(text='🔙 Назад', callback_data='back')
    start_posts.add(posts_in_market)
    start_posts.add(search_by_number)
    start_posts.add(back)
    return start_posts


# Клавиатура для работы админа с статистикой
def work_with_post(id_cod: str):
    print(id_cod)
    start_posts = InlineKeyboardMarkup()
    change_description = KeyboardButton(text='Редактировать описание', callback_data=f'change_description${id_cod}')
    delete_post = KeyboardButton(text='Удалить', callback_data=f'delete_post${id_cod}')
    back = KeyboardButton(text='🔙 Назад', callback_data='back')
    start_posts.add(change_description)
    start_posts.add(delete_post)
    start_posts.add(back)
    return start_posts


# Клавиатура для работы админа с статистикой
def work_with_reports(cod: str):
    start_posts = InlineKeyboardMarkup()
    change_description = KeyboardButton(text='Отклонить жалобу', callback_data=f'report_close')
    delete_post = KeyboardButton(text='Удалить пост', callback_data=f'report_delete${cod}')
    start_posts.add(change_description)
    start_posts.add(delete_post)
    return start_posts
