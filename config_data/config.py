import os
import sqlite3
from peewee import *
from dotenv import load_dotenv, find_dotenv



if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),

)



my_db = SqliteDatabase('bot.db')