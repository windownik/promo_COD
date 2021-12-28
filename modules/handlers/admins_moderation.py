from aiogram import types
from main import dp
from modules.handlers import users_functions
from modules.keyboards import market_kb, moderation_kb, category_kb, podcategory_kb, confirm_kb, back_kb
from modules.dispatcher import Admin_Work


# Start menu in moderation
@dp.callback_query_handler(text='category_back', state=Admin_Work.change_chat_moder)
@dp.callback_query_handler(text='category_back', state=Admin_Work.create_category)
@dp.callback_query_handler(text='my_bot', state='*')
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    users_functions.update_user_data(tg_id=call.from_user.id, name=call.from_user.first_name)
    await call.message.edit_text(text='Выберите что хотите поменять.', reply_markup=moderation_kb())
    await Admin_Work.moder.set()


# Редактор категорий предложений
@dp.callback_query_handler(state=Admin_Work.in_category, text='back_category')
@dp.callback_query_handler(text='category', state=Admin_Work.moder)
async def start_menu(call: types.CallbackQuery):
    data = users_functions.get_category()
    if 'category' not in str(data):
        await call.message.edit_text(text='Вы в редакторе категорий. Вот все ваши категории:',
                                     reply_markup=category_kb(data))
    else:
        await call.message.edit_text(text='У вас нет категорий создайте новую', reply_markup=category_kb())
    await Admin_Work.create_category.set()


# Start menu
@dp.callback_query_handler(text='add_category', state=Admin_Work.create_category)
async def start_menu(call: types.CallbackQuery):
    await call.message.edit_text('Введиет имя новой категории')
    await Admin_Work.create_category_name.set()


# Start menu
@dp.message_handler(state=Admin_Work.create_category_name)
async def start_menu(message: types.Message):
    users_functions.create_category(message.text)
    data = users_functions.get_category()
    if 'category' not in str(data):
        await message.answer(text='Вы в редакторе категорий. Вот все ваши категории:',
                             reply_markup=category_kb(data))
    else:
        await message.answer(text='У вас нет категорий создайте новую', reply_markup=category_kb())
    await Admin_Work.create_category.set()


# Start menu
@dp.callback_query_handler(text='backsub_', state=Admin_Work.create_category)
async def start_menu(call: types.CallbackQuery):
    users_functions.update_user_data(tg_id=call.from_user.id, name=call.from_user.first_name)
    await call.message.answer(text='Выберите что хотите поменять.', reply_markup=moderation_kb())
    await Admin_Work.moder.set()


# Start menu
@dp.callback_query_handler(state=Admin_Work.in_sub_category, text_contains='back_subc')
@dp.callback_query_handler(state=Admin_Work.delete_category, text_contains='backsub_')
@dp.callback_query_handler(state=Admin_Work.create_category)
async def start_menu(call: types.CallbackQuery):
    index = str(call.data)[9:]
    name_category = users_functions.get_name(int(index))['name']
    sub_categorys = users_functions.get_sub_category(int(index))
    if 'sub_category' in str(sub_categorys):
        await call.message.edit_text(f'Вы в редакторе категории <b>{name_category}</b>:\nВот все под категории '
                                     f'(магазины):',
                                     reply_markup=podcategory_kb(index=int(index)), parse_mode='html')
    else:
        await call.message.edit_text(f'Вы в редакторе категории <b>{name_category}</b>:\nВот все под категории '
                                     f'(магазины):',
                                     reply_markup=podcategory_kb(index=int(index), category=sub_categorys),
                                     parse_mode='html')
    await Admin_Work.in_category.set()


# Работаем в меню категориии
@dp.callback_query_handler(state=Admin_Work.in_sub_category_delete, text_contains='backsub_')
@dp.callback_query_handler(state=Admin_Work.in_category)
async def start_menu(call: types.CallbackQuery):
    if str(call.data).startswith('delete_category_'):
        index = str(call.data)[16:]
        name_category = users_functions.get_name(int(index))['name']
        users_functions.save_data1(tg_id=call.from_user.id, data=index)
        await call.message.edit_text(f"Вы точно хотите удалить категорию <b>{name_category}</b>?\n"
                                     f"Все вложенные категории будут удалены безвозвратно!",
                                     reply_markup=confirm_kb(index), parse_mode='html')
        await Admin_Work.delete_category.set()

    elif str(call.data).startswith('correct_name_'):
        index = str(call.data)[13:]
        name_category = users_functions.get_name(int(index))['name']
        users_functions.save_data1(tg_id=call.from_user.id, data=index)
        await call.message.edit_text(f"Вы меняете название категории <b>{name_category}</b>.\n"
                                     f"Введите новое название для категории", parse_mode='html')
        await Admin_Work.correct_name_category.set()

    elif str(call.data).startswith('add_podcategory_'):
        index = str(call.data)[16:]
        users_functions.save_data1(tg_id=call.from_user.id, data=index)
        await call.message.edit_text(f"Введите новое название магазина (подкатегории)")
        await Admin_Work.new_sub_category.set()
    else:
        category_index = str(call.data).split('_')[1]
        market_index = str(call.data).split('_')[2]
        market_name = users_functions.get_market_name(category_index=int(category_index),
                                                      market_index=int(market_index))
        users_functions.save_data1(tg_id=call.from_user.id, data=call.data)
        await call.message.edit_text(f"Вы в редакторе под категории (магазина): <b>{market_name}</b>.\n"
                                     f"Что хотите поменять?",
                                     parse_mode='html', reply_markup=market_kb(category_index=int(category_index),
                                                                               market_index=int(market_index)))
        await Admin_Work.in_sub_category.set()


# Удаляем категорию после подтверждение
@dp.callback_query_handler(state=Admin_Work.delete_category)
async def start_menu(call: types.CallbackQuery):
    index = str(call.data)[8:]
    retern_data = users_functions.delete_category(index)
    if 'ok' in str(retern_data):
        await call.message.edit_text('Категория успешно удалена')
        await call.message.answer(text='Выберите что хотите поменять.', reply_markup=moderation_kb())
        await Admin_Work.moder.set()
    else:
        await call.message.answer("При удалении произошла ошибка")


# Меняем название категории
@dp.message_handler(state=Admin_Work.correct_name_category)
async def start_menu(message: types.Message):
    index = users_functions.read_data1(message.from_user.id)
    users_functions.correct_name(index=int(index), name=message.text)
    data = users_functions.get_category()
    if 'category' not in str(data):
        await message.answer(text='Вы в редакторе категорий. Вот все ваши категории:',
                             reply_markup=category_kb(data))
    else:
        await message.answer(text='У вас нет категорий создайте новую', reply_markup=category_kb())
    await Admin_Work.create_category.set()


# Новый магазин в категории
@dp.message_handler(state=Admin_Work.new_sub_category)
async def start_menu(message: types.Message):
    index = users_functions.read_data1(message.from_user.id)
    users_functions.create_sub_category(name=message.text, index=index)
    name_category = users_functions.get_name(index)['name']
    sub_categorys = users_functions.get_sub_category(index)
    if 'sub_category' in str(sub_categorys):
        await message.answer(f'Вы в редакторе категории <b>{name_category}</b>:\nВот все под категории:',
                             reply_markup=podcategory_kb(index=int(index)), parse_mode='html')
    else:
        await message.answer(f'Вы в редакторе категории <b>{name_category}</b>:\nВот все под категории:',
                             reply_markup=podcategory_kb(index=int(index), category=sub_categorys),
                             parse_mode='html')
    await Admin_Work.in_category.set()


# Удаляем магазин
@dp.callback_query_handler(state=Admin_Work.in_sub_category, text_contains='delete_market_')
async def start_menu(call: types.CallbackQuery):
    category_index = str(call.data).split('_')[2]
    market_index = str(call.data).split('_')[3]
    market_name = users_functions.get_market_name(category_index=int(category_index), market_index=int(market_index))
    await call.message.edit_text(f'Вы точно хотите удалить под категорию (магазин) <b>{market_name}</b>?',
                                 parse_mode='html',
                                 reply_markup=confirm_kb(f'{category_index}_{market_index}'))
    await Admin_Work.in_sub_category_delete.set()


# Удаляем магазин
@dp.callback_query_handler(state=Admin_Work.in_sub_category_delete, text_contains='confirm_')
async def start_menu(call: types.CallbackQuery):
    category_index = str(call.data).split('_')[1]
    market_index = str(call.data).split('_')[2]
    users_functions.delete_sub_category(category_index=int(category_index), market_index=int(market_index))

    index = int(category_index)
    name_category = users_functions.get_name(index)['name']
    sub_categorys = users_functions.get_sub_category(index)
    await call.message.edit_text("Магазин успешно удален")
    if 'sub_category' in str(sub_categorys):
        await call.message.answer(f'Вы в редакторе категории <b>{name_category}</b>:\nВот все под категории:',
                                  reply_markup=podcategory_kb(index=int(index)), parse_mode='html')
    else:
        await call.message.answer(f'Вы в редакторе категории <b>{name_category}</b>:\nВот все под категории:',
                                  reply_markup=podcategory_kb(index=int(index), category=sub_categorys),
                                  parse_mode='html')
    await Admin_Work.in_category.set()


# Меняем имя магазина
@dp.callback_query_handler(state=Admin_Work.in_sub_category, text_contains='correct_name_')
async def start_menu(call: types.CallbackQuery):
    category_index = str(call.data).split('_')[2]
    market_index = str(call.data).split('_')[3]
    users_functions.save_data1(tg_id=call.from_user.id, data=f'{category_index}_{market_index}')
    await call.message.edit_text(f'Введиете новое название для подкатегории (магазина)')
    await Admin_Work.rename_sub_category.set()


# Новый магазин в категории
@dp.message_handler(state=Admin_Work.rename_sub_category)
async def start_menu(message: types.Message):
    await message.answer(f'Категория успешно переименовона')

    index = users_functions.read_data1(message.from_user.id)
    category_index = str(index).split('_')[0]
    market_index = str(index).split('_')[1]
    users_functions.correct_market_name(category_index=int(category_index), market_index=int(market_index),
                                        name=message.text)
    market_name = users_functions.get_market_name(category_index=int(category_index),
                                                  market_index=int(market_index))
    await message.answer(f"Вы в редакторе под категории (магазина): <b>{market_name}</b>.\n"
                         f"Что хотите поменять?",
                         parse_mode='html', reply_markup=market_kb(category_index=int(category_index),
                                                                   market_index=int(market_index)))
    await Admin_Work.in_sub_category.set()


@dp.callback_query_handler(text='moder_chat', state=Admin_Work.moder)
async def start_menu(call: types.CallbackQuery):
    data = users_functions.get_moder_chat()
    if 'no_chat' not in str(data):
        await call.message.edit_text(text='Вот чат модерации который уже сохранен.\n'
                                          f'{data["chat"]}\n'
                                          f'Если хотите его поменять отправьте мне новый chat_id группы '
                                          f'(пример: -123456789987)',
                                     reply_markup=back_kb())
    else:
        await call.message.edit_text(text='У вас не задан чат модерации отправьте мне chat_id группы '
                                          '(пример: -123456789987)',
                                     reply_markup=back_kb())
    await Admin_Work.change_chat_moder.set()


@dp.message_handler(state=Admin_Work.change_chat_moder)
async def start_menu(message: types.Message):
    if str(message.text[1:]).isdigit():
        users_functions.send_new_chat_id(message.text)
        await message.answer('Отлично я все сохранил', reply_markup=back_kb())
    else:
        await message.answer('Не вернный  формат chat id (пример: -123456789987)', reply_markup=back_kb())



