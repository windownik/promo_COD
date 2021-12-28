from aiogram import types
from main import dp
from modules.handlers import users_functions
from modules.keyboards import search_posts, work_with_post, category_front_kb, podcategory_front_kb
from modules.dispatcher import Admin_Statistic


# Первое меню поиск постов
@dp.callback_query_handler(text='back', state=Admin_Statistic.change_description_posts)
@dp.callback_query_handler(text='posts', state='*')
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    await call.message.edit_text(text='Здесь вы можете искать и редактировать посты.',
                                 reply_markup=search_posts())
    await Admin_Statistic.search_posts.set()


# Ищем пост по коду
@dp.callback_query_handler(text='search_by_number', state=Admin_Statistic.search_posts)
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных

    await call.message.edit_text(text='Введите номер промокода.')
    await Admin_Statistic.search_posts.set()


# Ищем пост в списке магазинов
@dp.callback_query_handler(text='posts_in_market', state=Admin_Statistic.search_posts)
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    all_categorys = users_functions.get_category()
    await call.message.edit_text(text='Выберите категорию.', reply_markup=category_front_kb(all_categorys))
    await Admin_Statistic.search_posts_category.set()


# Находим пост по тексту
@dp.message_handler(state=Admin_Statistic.search_posts)
async def start_menu(message: types.Message):
    data = users_functions.search_post_by_cod(message.text)
    if data:
        await message.answer(f'Я нашел предложение:\n'
                             f'Магазин: <b>{data[1]}</b>\n'
                             f'Код: <b>{data[2]}</b>\n'
                             f'Описание: <b>{data[3]}</b>\n'
                             f'Тип пользователей: <b>{data[4]}</b>\n'
                             f'Многоразовый/одноразовый: <b>{data[5]}</b>\n'
                             f'Дата создания: <b>{data[6]}</b>\n'
                             f'Статус: <b>{data[7]}</b>', parse_mode='html', reply_markup=work_with_post(data[0]))
        await Admin_Statistic.change_description_posts.set()
    else:
        await message.answer('Я ничего не нашел по данному коду. Попродуйте еще раз или нажмите /start')


# Меняем описание поста
@dp.callback_query_handler(text_contains='change_description$', state=Admin_Statistic.change_description_posts)
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    cod_id = call.data.split('$')[1]
    users_functions.save_data1(call.from_user.id, cod_id)
    await call.message.answer(text='Введите новое описание.')
    await Admin_Statistic.change_description_posts_get_text.set()


# Находим пост по тексту
@dp.message_handler(state=Admin_Statistic.change_description_posts_get_text)
async def start_menu(message: types.Message):
    data = users_functions.read_data1(message.from_user.id)
    description = message.text
    users_functions.update_post_description(cod=f"{data}", description=description)
    await message.answer('Описание изменено.')
    await message.answer(text='Здесь вы можете искать и редактировать посты.',
                         reply_markup=search_posts())
    await Admin_Statistic.search_posts.set()


# Меняем описание поста
@dp.callback_query_handler(text_contains='delete_post$', state=Admin_Statistic.change_description_posts)
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    cod_id = call.data.split('$')[1]
    users_functions.update_post_status(cod=cod_id, status=f'delete_{call.from_user.id}')
    await call.message.answer(text='Предложение удалено.')
    await call.message.answer(text='Здесь вы можете искать и редактировать посты.',
                              reply_markup=search_posts())
    await Admin_Statistic.search_posts.set()


# Ищем пост в списке магазинов
@dp.callback_query_handler(state=Admin_Statistic.search_posts_category)
async def start_menu(call: types.CallbackQuery):
    index = int(call.data.split("_")[1])
    # Обновляем данные пользователя в базе данных
    all_sub_categorys = users_functions.get_sub_category(index)
    await call.message.edit_text(text='Выберите магазин.',
                                 reply_markup=podcategory_front_kb(index, all_sub_categorys))
    await Admin_Statistic.search_posts_sub_category.set()


# Ищем пост в списке магазинов
@dp.callback_query_handler(state=Admin_Statistic.search_posts_sub_category)
async def start_menu(call: types.CallbackQuery):
    category_index = call.data.split('_')[1]
    market_index = call.data.split('_')[2]
    posts_10 = users_functions.get_10_post(category_index=category_index, market_index=market_index)
    for key in posts_10.keys():
        data = posts_10[key]
        await call.message.answer(f'Я нашел предложение:\n'
                                  f'Магазин: <b>{data["market_name"]}</b>\n'
                                  f'Код: <b>{data["cod"]}</b>\n'
                                  f'Описание: <b>{data["description"]}</b>\n',
                                  parse_mode='html', reply_markup=work_with_post(data['cod_id']))
    await Admin_Statistic.change_description_posts.set()
