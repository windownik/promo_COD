from aiogram import types
from main import dp
from aiogram.dispatcher import FSMContext
from modules.handlers import users_functions
from modules.keyboards import category_front_kb, podcategory_front_kb, user_second_kb, my_posts_kb, go_to_main, \
    feed_back, start_user_kb, work_with_reports
from modules.dispatcher import bot, User_Work
from modules.handlers.user_work_with_posts import next_post, previous_post, delete_my_post
from modules.handlers.text_functions import get_post_text_user


# Start menu
@dp.callback_query_handler(text='get_more_cod', state='*')
@dp.callback_query_handler(text='back_category', state=User_Work.pick_market)
@dp.callback_query_handler(text='get_cod', state='*')
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных
    data = users_functions.get_category()
    users_functions.update_user_data(tg_id=call.from_user.id, name=call.from_user.first_name)
    if 'category' not in str(data):
        await call.message.edit_text(text='📂 Прежде всего, выберите категорию, к которой относится желаемый промокод!',
                                     reply_markup=category_front_kb(data))
    else:
        await call.message.edit_text(text='📂 Прежде всего, выберите категорию, к которой относится желаемый промокод!',
                                     reply_markup=category_front_kb())
    await User_Work.pick_category.set()


@dp.callback_query_handler(state=User_Work.pick_category)
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
    await User_Work.pick_market.set()


@dp.callback_query_handler(state=User_Work.pick_market)
async def start_menu(call: types.CallbackQuery):
    post_data = users_functions.get_post(call.data, call.from_user.id)
    if 'no_cod' not in str(post_data):
        market_name = post_data['market_name']
        cod = post_data['cod']
        description = post_data['description']
        await call.message.edit_text(text=get_post_text_user(market_name=market_name, cod=cod, description=description),
                                     reply_markup=user_second_kb(post_data['cod_id']),
                                     parse_mode='html')
    else:
        await call.message.edit_text(f'К сажелению у нас нет промокода.', reply_markup=user_second_kb())
    await User_Work.cod_status.set()


# Работаем с моими промокодами
@dp.callback_query_handler(text='my_cod', state='*')
async def start_menu(call: types.CallbackQuery):
    all_posts = users_functions.get_my_favorite_posts(tg_id=call.from_user.id)
    number_of_posts = len(all_posts)
    if 'no_posts' in str(all_posts):
        await call.message.edit_text(text='У вас пока что нету промокодов', reply_markup=go_to_main())
    else:
        data = all_posts['1']
        text = get_post_text_user(cod=data[0], description=data[1], market_name=data[2])
        await call.message.edit_text(text=text, parse_mode='html', reply_markup=my_posts_kb(all_posts=number_of_posts,
                                                                                            cod_id=data[3]))
    await User_Work.my_promo_cods.set()


# Работаем с моими промокодами
@dp.callback_query_handler(state=User_Work.my_promo_cods)
async def start_menu(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    data = call.data
    if data.startswith('previous_'):
        await previous_post(call)
        await User_Work.my_promo_cods.set()
    elif data.startswith('next_'):
        await next_post(call)
        await User_Work.my_promo_cods.set()
    elif data.startswith('delpost_'):
        await delete_my_post(call)
        await User_Work.my_promo_cods.set()
    else:
        cod = call.data[7:]
        users_functions.save_data1(tg_id=call.from_user.id, data=cod)
        await call.message.edit_text(f'😣 Нам очень жаль, что вы столкнулись с проблемой.\n\n'
                                     f'Не могли бы вы написать, что именно у вас не работает сообщением ниже?',
                                     reply_markup=go_to_main())
        await User_Work.cod_feed_back.set()


@dp.callback_query_handler(text='feed_back', state='*')
async def start_menu(call: types.CallbackQuery):
    # Обновляем данные пользователя в базе данных

    await call.message.edit_text(text='✍️ Если у вас есть вопрос, пожелание или вы обнаружили ошибку - напишите '
                                      'нашему модератору по ссылке ниже, или нажав на кнопку!\n\n@Shmelev1982',
                                 reply_markup=feed_back())


# Жалоба на код
@dp.callback_query_handler(state=User_Work.cod_status, text_contains='bad_cod')
async def bad_cod(call: types.CallbackQuery):
    cod = call.data[7:]
    users_functions.save_data1(tg_id=call.from_user.id, data=cod)
    await call.message.edit_text(f'😣 Нам очень жаль, что вы столкнулись с проблемой.\n\n'
                                 f'Не могли бы вы написать, что именно у вас не работает сообщением ниже?',
                                 reply_markup=go_to_main())
    await User_Work.cod_feed_back.set()


# Жалоба на код
@dp.message_handler(state=User_Work.cod_feed_back)
async def bad_cod(message: types.Message, state: FSMContext):
    users_functions.send_report(report_text=message.text, tg_id=message.from_user.id)
    cod = users_functions.read_data1(message.from_user.id)
    moder_chat_id = users_functions.get_moder_chat()['chat']
    post = users_functions.get_post_by_index(cod)
    text = get_post_text_user(cod=post['cod'], description=post['description'], market_name=post['market_name'])
    try:
        await bot.send_message(chat_id=moder_chat_id, text=f'{text}\n\n'
                                                           f'---------------------\n'
                                                           f'Текст жалобы:\n' + message.text, parse_mode='html',
                               reply_markup=work_with_reports(cod))
    except Exception as ex:
        print('Ошибка доставки жалобы', ex)
    await message.answer('☺️ Большое спасибо за вашу жалобу, она поможет нам стать еще лучше!')
    users_functions.update_user_data(tg_id=message.from_user.id, name=message.from_user.first_name)
    await message.answer(text='👋🏻 Приветствуем вас в боте, который предназначен для раздачи промокодов всем '
                              'желающим!\n\n👇 Чтобы ориентироваться по боту, используйте клавиатуру ниже!')
    await message.answer(text="У нас есть канал!\n\nЧтобы не пропустить информацию о самых свежий промокодах, "
                              "подпишись на 👉  https://t.me/sovacode", reply_markup=start_user_kb())
    await state.finish()
