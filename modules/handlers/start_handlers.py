from aiogram import types
from main import dp
from aiogram.dispatcher.filters import Text
import logging
from modules.dispatcher import Admin_Work, Admin_POSTS, User_Work, Admin_Statistic
from aiogram.dispatcher import FSMContext
from modules.handlers import users_functions
from modules.keyboards import start_user_kb, start_admin_kb


# Start menu
@dp.message_handler(commands=['start'], state='*')
async def start_menu(message: types.Message, state: FSMContext):
    # Обновляем данные пользователя в базе данных
    admin_status = users_functions.is_admin(message.from_user.id)
    if admin_status:
        await message.answer(text='👋🏻 Привет администратор! Чем тебе помочь?', reply_markup=start_admin_kb())
    else:
        users_functions.update_user_data(tg_id=message.from_user.id, name=message.from_user.first_name)
        await message.answer(text='👋🏻 Приветствуем вас в боте, который предназначен для раздачи промокодов всем '
                                  'желающим!\n\n👇 Чтобы ориентироваться по боту, используйте клавиатуру ниже!')
        await message.answer(text="У нас есть канал!\n\nЧтобы не пропустить информацию о самых свежий промокодах, "
                                  "подпишись на 👉  https://t.me/sovacode", reply_markup=start_user_kb())
    await state.finish()


# Start menu
@dp.callback_query_handler(text='back', state=Admin_Statistic.search_posts)
@dp.callback_query_handler(text='back', state=Admin_Statistic.statistic_start)
@dp.callback_query_handler(text='back', state=Admin_POSTS.post_new_multicod)
@dp.callback_query_handler(text='category_back', state=Admin_Work.admins)
@dp.callback_query_handler(text='back_category', state=Admin_POSTS.new_post)
@dp.callback_query_handler(text='back', state=Admin_Work.moder)
async def start_menu(call: types.CallbackQuery, state: FSMContext):
    # Обновляем данные пользователя в базе данных
    admin_status = users_functions.is_admin(call.from_user.id)
    if admin_status:
        await call.message.edit_text(text='👋🏻 Привет администратор! Чем тебе помочь?', reply_markup=start_admin_kb())
    await state.finish()


# Start menu
@dp.callback_query_handler(text='back_category', state=User_Work.my_promo_cods)
@dp.callback_query_handler(text='back_category', state=User_Work.reg_premium_user)
@dp.callback_query_handler(text='back_category', state=User_Work.pick_category_premium)
@dp.callback_query_handler(text='back_category', state=User_Work.pick_category)
async def start_menu(call: types.CallbackQuery, state: FSMContext):
    # Обновляем данные пользователя в базе данных
    users_functions.update_user_data(tg_id=call.from_user.id, name=call.from_user.first_name)
    await call.message.answer(text='👋🏻 Приветствуем вас в боте, который предназначен для раздачи промокодов всем '
                              'желающим!\n\n👇 Чтобы ориентироваться по боту, используйте клавиатуру ниже!')
    await call.message.answer(text="У нас есть канал!\n\nЧтобы не пропустить информацию о самых свежий промокодах, "
                              "подпишись на 👉  https://t.me/sovacode", reply_markup=start_user_kb())
    await state.finish()


# Start menu
@dp.callback_query_handler(text='go_to_main', state='*')
@dp.callback_query_handler(text='as_user', state='*')
async def start_menu(call: types.CallbackQuery, state: FSMContext):
    # Обновляем данные пользователя в базе данных
    users_functions.update_user_data(tg_id=call.from_user.id, name=call.from_user.first_name)
    await call.message.edit_text(text='👋🏻 Приветствуем вас в боте, который предназначен для раздачи промокодов всем '
                                      'желающим!\n\n👇 Чтобы ориентироваться по боту, используйте клавиатуру ниже!')
    await call.message.answer(text="У нас есть канал!\n\nЧтобы не пропустить информацию о самых свежий промокодах, "
                                   "подпишись на 👉  https://t.me/sovacode", reply_markup=start_user_kb())
    await state.finish()


# Start menu
@dp.message_handler(commands=['create_db'], state='*')
async def start_menu(message: types.Message):
    # Создаем все таблицы в бд
    users_functions.create_tables()

    await message.answer(text='Я создал все базы данных')


# Start menu
@dp.message_handler(commands=['new_admin_is'], state='*')
async def start_menu(message: types.Message):
    users_functions.create_admin(message.from_user.id)

    await message.answer(text='Я создал нового админа')


# Start menu
@dp.message_handler(commands=['admin_to_user'], state='*')
async def start_menu(message: types.Message):
    users_functions.delete_admin(message.from_user.id)

    await message.answer(text='Я удалил админа')


# Cancel all process
@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    await message.reply('Процес отменен. Все данные стерты. Что бы начать все с начала нажми /start',
                        reply_markup=types.ReplyKeyboardRemove())
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
