from aiogram import types
from main import dp
from modules.handlers import users_functions
from modules.keyboards import category_front_kb, podcategory_front_kb, user_second_kb, my_posts_kb, go_to_main, \
    feed_back
from modules.dispatcher import bot, User_Work
from modules.handlers.user_work_with_posts import next_post, previous_post, delete_my_post
from modules.handlers.text_functions import get_post_text_user


# async def
