from aiogram import types
from main import dp
from modules.handlers import users_functions
from modules.keyboards import back_kb, new_admin_kb
from modules.dispatcher import Admin_Work


# Work with admins
@dp.callback_query_handler(text='category_back', state=Admin_Work.search)
@dp.callback_query_handler(text='admins', state='*')
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    users_functions.update_user_data(tg_id=call.from_user.id, name=call.from_user.first_name)
    await call.message.edit_text(text='Введите телеграм id, или телефон пользователя.', reply_markup=back_kb())
    await Admin_Work.admins.set()


# Search user
@dp.message_handler(state=Admin_Work.admins)
async def start_menu(message: types.Message):
    search_user = users_functions.find_user(message.text)
    if search_user:
        await message.answer(f"Пользователь найден:\n"
                             f"Имя. <b>{search_user[2]}</b>\n"
                             f"Teлеграм id. <b>{search_user[1]}</b>\n"
                             f"Телефон: <b>{search_user[5]}</b>\n"
                             f"Статус: <b>{search_user[3]}</b>\n"
                             f"Последний вход  в бот: <b>{search_user[4]}</b>",
                             reply_markup=new_admin_kb(search_user[1]), parse_mode='html')
        await Admin_Work.search.set()
    else:
        await message.answer('Пользователь с такими данными не найден.', reply_markup=back_kb())


# Удаляем пользователя из админов
@dp.callback_query_handler(text_contains='delete_admin_', state=Admin_Work.search)
async def start_menu(call: types.CallbackQuery):
    tg_id = str(call.data).split('_')[2]
    users_functions.delete_admin(int(tg_id))
    await call.message.edit_text(text='Пользователь удален из админов.')
    await call.message.answer(text='Введите телеграм id, или телефон пользователя.', reply_markup=back_kb())
    await Admin_Work.admins.set()


# Делаем пользователя админом
@dp.callback_query_handler(text_contains='set_admin_', state=Admin_Work.search)
async def start_menu(call: types.CallbackQuery):
    tg_id = str(call.data).split('_')[2]
    users_functions.create_admin(int(tg_id))
    await call.message.edit_text(text='Пользователю даны права админа.')
    await call.message.answer(text='Введите телеграм id, или телефон пользователя.', reply_markup=back_kb())
    await Admin_Work.admins.set()


# Делаем пользователя админом
@dp.callback_query_handler(text_contains='ban_user_', state=Admin_Work.search)
async def start_menu(call: types.CallbackQuery):
    tg_id = str(call.data).split('_')[2]
    users_functions.ban_user(int(tg_id))
    await call.message.edit_text(text='Пользователь заблокирован.')
    await call.message.answer(text='Введите телеграм id, или телефон пользователя.', reply_markup=back_kb())
    await Admin_Work.admins.set()
