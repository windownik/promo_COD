from aiogram import types
from main import dp
from modules.keyboards import new_admin_stat, back_kb, stat_posts
from modules.dispatcher import Admin_Statistic
from modules.handlers import users_functions


# Первое меню статистики
@dp.callback_query_handler(text='back', state=Admin_Statistic.statistic_posts)
@dp.callback_query_handler(text='category_back', state=Admin_Statistic.statistic_users)
@dp.callback_query_handler(text='inform', state='*')
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    await call.message.edit_text(text='Какую статистику вы хотите получить?',
                                 reply_markup=new_admin_stat())
    await Admin_Statistic.statistic_start.set()


# Статистика пользователей
@dp.callback_query_handler(text='users_stat', state=Admin_Statistic.statistic_start)
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    users_statistic = users_functions.get_users_statistic()
    all_users_number = users_statistic['all_users_number']
    all_new_users_number = users_statistic['all_new_users_number']
    active_users_number = users_statistic['active_users_number']
    await call.message.edit_text(
        text=f'На телеграм бот за все время было подписано <b>{all_users_number}</b>.\n'
             f'Новых пользователей за месяц: <b>{all_new_users_number}</b>\n'
             f'Активных пользователей за месяц: <b>{active_users_number}</b>.',
        reply_markup=back_kb(), parse_mode='html')
    await Admin_Statistic.statistic_users.set()


# Статистика постов
@dp.callback_query_handler(text='category_back', state=Admin_Statistic.statistic_posts_market)
@dp.callback_query_handler(text='category_back', state=Admin_Statistic.statistic_posts_category)
@dp.callback_query_handler(text='category_back', state=Admin_Statistic.statistic_posts_bad_cod)
@dp.callback_query_handler(text='posts_stat', state=Admin_Statistic.statistic_start)
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    await call.message.edit_text(text=f'Какую статистику вы хотите получить?',
                                 reply_markup=stat_posts())
    await Admin_Statistic.statistic_posts.set()


# Статистика постов - количество брака
@dp.callback_query_handler(text='bad_cod', state=Admin_Statistic.statistic_posts)
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    bad_cod_statistic = users_functions.get_bad_cod_statistic()
    all_reports_number = bad_cod_statistic['all_reports_number']
    all_new_reports = bad_cod_statistic['all_new_reports']
    await call.message.edit_text(text=f'За последний месяц было полученож жалоб: <b>{all_new_reports}</b>\n'
                                      f'Всего за все время было получено жалоб: <b>{all_reports_number}</b>',
                                 reply_markup=back_kb(), parse_mode='html')
    await Admin_Statistic.statistic_posts_bad_cod.set()


# Статистика постов - топ категорий
@dp.callback_query_handler(text='top_category', state=Admin_Statistic.statistic_posts)
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    get_categorys = users_functions.get_top_categorys()
    text = 'Вот топ категорий за все время:\n'
    for market in get_categorys:
        text = text + f'{market[1]}: <b>{market[2]}</b>\n'
    await call.message.edit_text(text=text, reply_markup=back_kb(), parse_mode='html')
    await Admin_Statistic.statistic_posts_category.set()


# Статистика постов - топ магазинов
@dp.callback_query_handler(text='top_market', state=Admin_Statistic.statistic_posts)
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    await call.message.edit_text(text=f'Вот самые популярные магазины за последний месяц.'
                                      f'1.  - 1000 в избранное'
                                      f'2.'
                                      f'3.',
                                 reply_markup=back_kb())
    await Admin_Statistic.statistic_posts_market.set()
