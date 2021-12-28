import csv
from modules.dispatcher import bot


# Проверяем файл csv
async def read_csv(chat_id):
    try:
        with open('cods.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            i = 0
            for row in spamreader:
                i += 1
                if i < 3:
                    await bot.send_message(chat_id=chat_id, text=', '.join(row))
                else:
                    break
    except:
        await bot.send_message(chat_id=chat_id, text="Произошла ошибка при работе с файлом")


# Читаем первый код из файла
def read_csv_one_line():
    with open('cods.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            text = ', '.join(row)
            return text


# Читаем первый код из файла
def read_csv_all():
    with open('cods.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        text = ''
        for row in spamreader:
            text = text + ', '.join(row) + '|'

        return text[:-1]
