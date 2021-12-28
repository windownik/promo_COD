from aiogram import Bot, Dispatcher
from modules.setings import MainSettings
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

import logging

constant = MainSettings()
telegram_token = constant.tg_token()


storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(telegram_token)
dp = Dispatcher(bot, storage=storage)


# Welcome form
class Admin_Work(StatesGroup):
    moder = State()
    create_category = State()
    create_category_name = State()
    in_category = State()
    delete_category = State()
    correct_name_category = State()

    change_chat_moder = State()

    new_sub_category = State()
    in_sub_category = State()
    in_sub_category_delete = State()
    rename_sub_category = State()

    admins = State()
    search = State()


# Welcome form
class Admin_POSTS(StatesGroup):
    new_post = State()
    new_post_type_sending_data = State()
    new_post_input_description = State()
    new_post_catch_text = State()
    new_post_catch_cod = State()
    new_post_type_time = State()
    new_post_type_users = State()
    post_new_post = State()

    new_post_catch_file = State()
    new_post_multicod_text = State()
    new_post_multicod_save_text = State()
    new_post_multicod_user_type = State()
    post_new_multicod = State()


class User_Work(StatesGroup):
    pick_category = State()
    pick_market = State()
    cod_status = State()
    my_promo_cods = State()

    cod_feed_back = State()

    reg_premium_user = State()
    pick_category_premium = State()
    pick_market_premium = State()
    cod_status_premium = State()


class Admin_Statistic(StatesGroup):
    statistic_start = State()
    statistic_users = State()

    statistic_posts = State()
    statistic_posts_bad_cod = State()
    statistic_posts_category = State()
    statistic_posts_market = State()

    search_posts = State()
    change_description_posts = State()
    change_description_posts_get_text = State()

    search_posts_category = State()
    search_posts_sub_category = State()
    search_posts_market_posts = State()
