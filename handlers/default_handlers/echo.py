from telebot.types import Message
from loader import bot
import openai
import os
from database.data import *
from database.meet_process import *


openai.api_key = os.getenv('KEY')
requests_array = []

@bot.message_handler(content_types=['text'])
def bot_echo(message: Message):
    #запросы
    user_request = message.text
    if user_request.startswith("https://meet.google.com/"):
        process_google_meet_link(user_request)
    file_request = read_file_request()
    #формируем и закидываем в массив запросы
    request_obj = {
        "user_request": user_request,
        "file_request": file_request,
    }
    requests_array.append(request_obj)
    # Функция для обработки запроса в GPT
    response = process_gpt_request(file_request, user_request)

    bot.send_message(message.chat.id, response)