import os
import requests
import openai
from loader import bot
from config_data.config import *
import textwrap

openai.api_key = os.getenv('KEY')


def read_file_request():
    """
    Функция для чтения запроса из файла
    :return:
    """
    with open("/Users/mymacbook/PycharmProjects/pythonProject/BotRecordCall/transcribe.txt", "r", encoding="utf-8") as file:
        file_request = file.read()
    return file_request


def split_text_into_chunks(text, max_length):
    """
    Разбивает текст на части по предложениям.
    """
    sentences = text.split('. ')
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len(chunk) + len(sentence) + 1 > max_length:
            chunks.append(chunk)
            chunk = ""
        chunk += sentence + ". "
    if chunk:
        chunks.append(chunk)
    return chunks


def process_gpt_request(file_request, user_request, max_length=4096):
    """
    Функция для обработки запроса в GPT
    :param file_request:
    :param user_request:
    :return:
    """

    #Разбиваем файловый запрос на части
    chunks = split_text_into_chunks(file_request, max_length - len(user_request) - 50)  # 50 - примерный буфер
    final_response = ""

    for chunk in chunks:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": chunk},
                {"role": "user", "content": user_request},
            ],
        )

        if response and response.choices:
            reply = response['choices'][0]['message']['content']
            final_response += reply + " "

    return final_response.strip()

    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": file_request},
    #         {"role": "user", "content": user_request},
    #
    #     ],
    # )
    # if response and response.choices:  # если есть ответ и есть варианты ответов(n=1)
    #     #reply = response.choices[0].text.strip()  # пробелы обрезаем
    #     reply = response['choices'][0]['message']['content']
    # else:
    #     reply = 'smth went wrong'
    # return reply



def is_valid_google_meet_link(link):
    try:
        response = requests.head(link)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
