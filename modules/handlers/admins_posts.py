from aiogram import types
from main import dp
from modules.handlers.text_functions import get_post_text, save_post
from modules.handlers import users_functions
from modules.keyboards import category_front_kb, podcategory_front_kb, type_send_cod, post_type, post_user_type, \
    send_post_kb, start_admin_kb
from modules.dispatcher import Admin_POSTS


# Работаем с репортами на посты
@dp.callback_query_handler(text='report_close', state="*")
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    await call.message.edit_text(text='Жалоба отклонена')


# Работаем с репортами на посты
@dp.callback_query_handler(text_contains='report_delete$', state="*")
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    cod = call.data.split('$')[1]
    cod = cod.split("_")
    if len(cod) == 4:
        await call.message.edit_text(text='Мульти предложение пока что нельзя удалить.')
    else:
        users_functions.update_post_status(cod, status=f'delete_{call.from_user.id}')
        await call.message.edit_text(text='Предложение удалено')


# Меню создания предложений
@dp.callback_query_handler(text='back_category', state=Admin_POSTS.new_post_type_sending_data)
@dp.callback_query_handler(text='create_post', state='*')
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    data = users_functions.get_category()
    users_functions.update_user_data(tg_id=call.from_user.id, name=call.from_user.first_name)
    if 'category' not in str(data):
        await call.message.edit_text(text='Здесь вы создаете новые предложения. Выберите категорию.',
                                     reply_markup=category_front_kb(data))
    else:
        await call.message.edit_text(text='Здесь вы создаете новые предложения. Выберите категорию.',
                                     reply_markup=category_front_kb())
    await Admin_POSTS.new_post.set()


# Start menu
@dp.callback_query_handler(state=Admin_POSTS.new_post)
async def start_menu(call: types.CallbackQuery):
    index = str(call.data)[9:]
    name_category = users_functions.get_name(index)['name']
    sub_categorys = users_functions.get_sub_category(index)
    await call.message.edit_text(f'Вы создаете новое предложение в категории {name_category}. Выберите под категорию.',
                                 reply_markup=podcategory_front_kb(index=int(index), category=sub_categorys),
                                 parse_mode='html')
    await Admin_POSTS.new_post_type_sending_data.set()


# Start menu

@dp.callback_query_handler(state=Admin_POSTS.new_post_type_sending_data)
async def start_menu(call: types.CallbackQuery):
    index = str(call.data)[12:]
    users_functions.save_data1(tg_id=call.from_user.id, data=index)
    await call.message.edit_text(f'Выберите тип отпраки данных', reply_markup=type_send_cod())
    await Admin_POSTS.new_post_input_description.set()


# Start menu
@dp.callback_query_handler(state=Admin_POSTS.new_post_input_description, text='get_text')
async def start_menu(call: types.CallbackQuery):
    await call.message.edit_text(f'Введите текст описания промокода.')
    await Admin_POSTS.new_post_catch_text.set()


# Новый магазин в категории
@dp.message_handler(state=Admin_POSTS.new_post_catch_text)
async def start_menu(message: types.Message):
    users_functions.save_data2(tg_id=message.from_user.id, data=message.text)
    await message.answer(f'Введите промокод.')
    await Admin_POSTS.new_post_catch_cod.set()


# Новый магазин в категории
@dp.message_handler(state=Admin_POSTS.new_post_catch_cod)
async def start_menu(message: types.Message):
    users_functions.save_data3(tg_id=message.from_user.id, data=message.text)
    await message.answer(f'Выберите тип поста.', reply_markup=post_type())
    await Admin_POSTS.new_post_type_time.set()


# Start menu
@dp.callback_query_handler(state=Admin_POSTS.new_post_type_time)
async def start_menu(call: types.CallbackQuery):
    users_functions.save_data4(tg_id=call.from_user.id, data=call.data)
    await call.message.edit_text(f'Выберите кто будет получать промокод.', reply_markup=post_user_type())
    await Admin_POSTS.new_post_type_users.set()


# Start menu
@dp.callback_query_handler(state=Admin_POSTS.new_post_type_users)
async def start_menu(call: types.CallbackQuery):
    user_id = call.from_user.id
    users_functions.save_data5(tg_id=call.from_user.id, data=call.data)
    # получаем текст поста?
    text = get_post_text(user_id)
    await call.message.answer(text=text, parse_mode='html')
    await call.message.answer(f'Опубликовать пост?', reply_markup=send_post_kb())
    await Admin_POSTS.post_new_post.set()


# Start menu
@dp.callback_query_handler(state=Admin_POSTS.post_new_post, text='confirm')
async def start_menu(call: types.CallbackQuery):
    # получаем текст поста?
    save_post(user_id=call.from_user.id)
    await call.message.edit_text(f'Пост опубликован')
    await call.message.answer(text='👋🏻 Привет администратор! Чем тебе помочь?', reply_markup=start_admin_kb())
