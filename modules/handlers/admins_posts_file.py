from aiogram import types
from main import dp
from modules.handlers.text_functions import get_multipost_text, save_multipost
from modules.handlers import users_functions
from modules.keyboards import post_user_type, send_post_kb, start_admin_kb
from modules.dispatcher import Admin_POSTS
from modules.csv_reader import read_csv


# Start menu
@dp.callback_query_handler(state=Admin_POSTS.new_post_input_description, text='get_file')
async def start_menu(call: types.CallbackQuery):
    await call.message.edit_text(f'Отправьте мне Файл csv с столбиком промокодов')
    await Admin_POSTS.new_post_catch_file.set()


# Новый магазин в категории
@dp.message_handler(state=Admin_POSTS.new_post_catch_file, content_types=types.ContentType.DOCUMENT)
async def start_menu(message: types.Message):
    await message.document.download(destination_file='cods.csv')
    # file_id = message.document.file_id
    # users_functions.save_data2(tg_id=message.from_user.id, data=file_id)
    await read_csv(message.chat.id)
    await message.answer(f'Вот несколько кодов которые я нашел в файле.\nЕсли все верно нажмите "Да!"',
                         reply_markup=send_post_kb())
    await Admin_POSTS.new_post_multicod_text.set()


# Start menu
@dp.callback_query_handler(state=Admin_POSTS.new_post_multicod_text)
async def start_menu(call: types.CallbackQuery):
    if call.data == 'confirm':
        await call.message.edit_text(f'Введите текст общего описания промокодов.')
        await Admin_POSTS.new_post_multicod_save_text.set()
    elif call.data == 'back':
        await call.message.edit_text(f'Отправьте мне Файл csv с столбиком промокодов')
        await Admin_POSTS.new_post_catch_file.set()


# Start menu
@dp.message_handler(state=Admin_POSTS.new_post_multicod_save_text)
async def start_menu(message: types.Message):
    users_functions.save_data2(tg_id=message.from_user.id, data=message.text)
    await message.answer(f'Выберите кто будет получать промокод.', reply_markup=post_user_type())
    await Admin_POSTS.new_post_multicod_user_type.set()


# Start menu
@dp.callback_query_handler(state=Admin_POSTS.new_post_multicod_user_type)
async def start_menu(call: types.CallbackQuery):
    user_id = call.from_user.id
    users_functions.save_data3(tg_id=call.from_user.id, data=call.data)
    # получаем текст поста?
    text = get_multipost_text(user_id)
    await call.message.answer(text=text, parse_mode='html')
    await call.message.answer(f'Опубликовать предложение?', reply_markup=send_post_kb())
    await Admin_POSTS.post_new_multicod.set()


# Start menu
@dp.callback_query_handler(state=Admin_POSTS.post_new_multicod, text='confirm')
async def start_menu(call: types.CallbackQuery):
    # получаем текст поста?
    save_multipost(user_id=call.from_user.id)
    await call.message.edit_text(f'Предложение опубликовано')
    await call.message.answer(text='👋🏻 Привет администратор! Чем тебе помочь?', reply_markup=start_admin_kb())
