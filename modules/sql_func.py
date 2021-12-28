import psycopg2
from modules.dispatcher import constant


# Новый юзер создает таблицу в бд
def new_table():
    try:
        db = psycopg2.connect(
            host=constant.db_host(),
            user=constant.user_db(),
            password=constant.password_db(),
            database=constant.db_name()
        )
        with db.cursor() as cursor:
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS all_users (
             id SERIAL PRIMARY KEY,
             tg_id INTEGER UNIQUE,
             user_name TEXT,
             status TEXT,
             activity TEXT,
             phone TEXT)''')
            db.commit()
    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Делаем запись новой строки в базу данных
def first_note(table: str, id_name: str, data):
    try:
        db = psycopg2.connect(
            host=constant.db_host(),
            user=constant.user_db(),
            password=constant.password_db(),
            database=constant.db_name()
        )
        with db.cursor() as cursor:
            cursor.execute(f"INSERT INTO {table} ({id_name}) VALUES ('{data}') ON CONFLICT DO NOTHING;")
            db.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Делаем запись новой строки в базу данных
def update_data(table: str, id_name: str, data, name: str, id_data):
    try:
        db = psycopg2.connect(
            host=constant.db_host(),
            user=constant.user_db(),
            password=constant.password_db(),
            database=constant.db_name()
        )
        with db.cursor() as cursor:
            cursor.execute(f"UPDATE {table} SET {name}=('{data}') WHERE {id_name}='{id_data}'")
            db.commit()

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()


# Делаем запись новой строки в базу данных
def read_all(
        name: str = '*',
        table: str = 'all_users'):
    try:

        db = psycopg2.connect(
            host=constant.db_host(),
            user=constant.user_db(),
            password=constant.password_db(),
            database=constant.db_name()
        )
        with db.cursor() as cursor:
            cursor.execute(f'SELECT {name} FROM {table}')
            data = cursor.fetchall()
            return data

    except Exception as _ex:
        print('[INFO] Error while working with db', _ex)
    finally:
        if db:
            db.close()
