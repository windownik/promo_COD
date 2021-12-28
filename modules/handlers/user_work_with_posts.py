from aiogram import types
from modules.handlers import users_functions
from modules.keyboards import go_to_main, my_posts_kb
from modules.handlers.text_functions import get_post_text_user


# Следующий пост
async def next_post(call: types.CallbackQuery):
    data = call.data
    last_post = int(data.split('_')[1])
    all_posts = users_functions.get_my_favorite_posts(tg_id=call.from_user.id)
    number_of_posts = len(all_posts)
    if last_post == number_of_posts:
        return
    else:
        last_post += 1
    data = all_posts[str(last_post)]
    text = get_post_text_user(cod=data[0], description=data[1], market_name=data[2])
    await call.message.edit_text(text=text, parse_mode='html', reply_markup=my_posts_kb(all_posts=number_of_posts,
                                                                                        last_post=last_post,
                                                                                        cod_id=data[3]))


# Пред идущий пост
async def previous_post(call: types.CallbackQuery):
    data = call.data
    last_post = int(data.split('_')[1])
    all_posts = users_functions.get_my_favorite_posts(tg_id=call.from_user.id)
    number_of_posts = len(all_posts)
    if last_post == 1:
        return
    else:
        last_post -= 1

    data = all_posts[str(last_post)]
    text = get_post_text_user(cod=data[0], description=data[1], market_name=data[2])
    await call.message.edit_text(text=text, parse_mode='html', reply_markup=my_posts_kb(all_posts=number_of_posts,
                                                                                        last_post=last_post,
                                                                                        cod_id=data[3]))


# Пред идущий пост
async def delete_my_post(call: types.CallbackQuery):
    data = call.data
    last_post = int(data.split('_')[1])
    all_posts = users_functions.get_my_favorite_posts(tg_id=call.from_user.id)
    number_of_posts = len(all_posts)
    users_functions.delete_my_post(tg_id=call.from_user.id, post_data=all_posts[str(last_post)][3])

    all_posts_new = users_functions.get_my_favorite_posts(tg_id=call.from_user.id)
    if 'no_posts' in str(all_posts_new):
        await call.message.edit_text(text='У вас пока что нету промокодов', reply_markup=go_to_main())
    else:
        if last_post == 1:
            number = 1
        else:
            number = last_post - 1
        data = all_posts[str(number)]
        text = get_post_text_user(cod=data[0], description=data[1], market_name=data[2])
        await call.message.answer(text=text, parse_mode='html',
                                     reply_markup=my_posts_kb(all_posts=number_of_posts - 1,
                                                              last_post=number,
                                                              cod_id=data[3]))
