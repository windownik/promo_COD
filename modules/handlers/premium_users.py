from aiogram import types
from main import dp
from modules.handlers import users_functions
from modules.keyboards import category_front_kb, send_contact_kb, user_second_kb, my_posts_kb, go_to_main, \
    podcategory_front_kb
from modules.dispatcher import bot, User_Work
from modules.handlers.user_work_with_posts import next_post, previous_post, delete_my_post
from modules.handlers.text_functions import get_post_text_user


# Start menu
@dp.callback_query_handler(text='premium_cod_for_u', state='*')
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    premium_status = users_functions.is_premium(call.from_user.id)
    if premium_status:
        data = users_functions.get_category()
        users_functions.update_user_data(tg_id=call.from_user.id, name=call.from_user.first_name)
        if 'category' not in str(data):
            await call.message.edit_text(
                text='📂 Прежде всего, выберите категорию, к которой относится желаемый промокод!',
                reply_markup=category_front_kb(data))
        else:
            await call.message.edit_text(
                text='📂 Прежде всего, выберите категорию, к которой относится желаемый промокод!',
                reply_markup=category_front_kb())
        await User_Work.pick_category_premium.set()
    else:
        await call.message.answer(text='Что бы получать специальные предложения. Поделитесь с нами своим контактом.',
                                  reply_markup=send_contact_kb)
        await User_Work.reg_premium_user.set()


# Start menu
@dp.message_handler(content_types=['contact'], state=User_Work.reg_premium_user)
async def start_menu(message: types.Message):
    await message.answer(text='Теперь вы зарегестрированы',
                              reply_markup=types.ReplyKeyboardRemove())
    data = users_functions.get_category()
    phone = message.contact.phone_number
    users_functions.save_phone(message.from_user.id, phone=phone)
    if 'category' not in str(data):
        await message.answer(
            text='📂 Прежде всего, выберите категорию, к которой относится желаемый промокод!',
            reply_markup=category_front_kb(data))
    else:
        await message.answer(
            text='📂 Прежде всего, выберите категорию, к которой относится желаемый промокод!',
            reply_markup=category_front_kb())
    await User_Work.pick_category_premium.set()


# Start menu
@dp.message_handler(state=User_Work.reg_premium_user)
async def start_menu(message: types.Message):
    await message.answer(text='Пожалуйста нажмите на кнопку', reply_markup=send_contact_kb)
    await User_Work.reg_premium_user.set()


@dp.callback_query_handler(state=User_Work.pick_category_premium)
async def start_menu(call: types.CallbackQuery):
    index = str(call.data).split("_")[1]
    sub_categorys = users_functions.get_sub_category(int(index))
    if 'sub_category' in str(sub_categorys):
        await call.message.edit_text(f'Отлично. Теперь выберите подкатегорию (магазин):',
                                     reply_markup=podcategory_front_kb(index=int(index)), parse_mode='html')
    else:
        await call.message.edit_text(f'Отлично. Теперь выберите подкатегорию (магазин):',
                                     reply_markup=podcategory_front_kb(index=int(index), category=sub_categorys),
                                     parse_mode='html')
    await User_Work.pick_market_premium.set()


@dp.callback_query_handler(state=User_Work.pick_market_premium)
async def start_menu(call: types.CallbackQuery):
    post_data = users_functions.get_premium_post(call.data, call.from_user.id)
    if 'no_cod' not in str(post_data):
        market_name = post_data['market_name']
        cod = post_data['cod']
        description = post_data['description']
        await call.message.edit_text(text=get_post_text_user(market_name=market_name, cod=cod, description=description),
                                     reply_markup=user_second_kb(),
                                     parse_mode='html')
    else:
        await call.message.edit_text(f'К сажелению у нас нет промокода.', reply_markup=user_second_kb())
    await User_Work.cod_status_premium.set()
