import os
import requests
import openai
from loader import bot
from config_data.config import *

openai.api_key = os.getenv('KEY')


# class BaseModel(Model):
#     class Meta:
#         database = my_db
#         db_table = 'table'
#
#
# class User_Data(BaseModel):
#     user_telegram_id = IntegerField()
#
#
# def create_db() -> None:
#     """
#     Функция создает базу данных, если она отсутствует.
#     :return:
#     """
#     try:
#         my_db.connect()
#         User_Data.create_table()
#     except InternalError as px:
#         print(str(px))
#
#
# def add_user_data(user_telegram_id) -> None:
#     """
#     Функция создает запись в базе данных.
#     :param user_telegram_id:
#     :param command:
#     :param request_time:
#     :param text_for_database:
#     :return:
#     """
#
#     with my_db:
#         User_Data.create(user_telegram_id=user_telegram_id,
#                             user_command=command,
#                             user_time_request=request_time,
#                             user_hotels_list=text_for_database
#                             )


def read_file_request():
    """
    Функция для чтения запроса из файла
    :return:
    """
    with open("/Users/mymacbook/PycharmProjects/pythonProject/BotRecordCall/database/transcribe.txt", "r", encoding="utf-8") as file:
        file_request = file.read()
    return file_request

def process_gpt_request(file_request, user_request):
    """
    Функция для обработки запроса в GPT
    :param file_request:
    :param user_request:
    :return:
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": file_request},
            {"role": "user", "content": user_request},

        ],
    )
    if response and response.choices:  # если есть ответ и есть варианты ответов(n=1)
        #reply = response.choices[0].text.strip()  # пробелы обрезаем
        reply = response['choices'][0]['message']['content']
    else:
        reply = 'smth went wrong'
    return reply

def is_valid_google_meet_link(link):
    try:
        response = requests.head(link)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False