from telebot.types import Message
from loader import bot
import openai
import os
from database.data import *
from database.meet_process import process_google_meet_link


openai.api_key = os.getenv('KEY')
requests_array = []

MAX_MESSAGE_LENGTH = 4096
@bot.message_handler(content_types=['text'])
def bot_echo(message: Message):
    #запросы
    user_request = message.text
    if user_request.startswith("/meet "):
        handle_meet_command(message)  # Вызываем обработку команды /meet
    else:
        file_request = read_file_request()
        #формируем и закидываем в массив запросы
        request_obj = {
            "user_request": user_request,
            "file_request": file_request,
        }
        requests_array.append(request_obj)
        # Функция для обработки запроса в GPT
        response = process_gpt_request(file_request, user_request)

        # Разбиваем ответ на части и отправляем каждую часть
        for chunk in split_text_into_chunks(response, MAX_MESSAGE_LENGTH):
            bot.send_message(message.chat.id, chunk)
        #bot.send_message(message.chat.id, response)


@bot.message_handler(commands=['meet'])
def handle_meet_command(message):
    #global max_participants
    user_id = message.chat.id

    # Разделяем сообщение на аргументы
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(user_id, "Использование: /meet <кол-во участников> <ссылка>")
        return

    # Первый аргумент - команда, второй - ссылка
    command, num_participants, link = args

    if command == "/meet":
        try:
            max_participants = int(num_participants)
        except ValueError:
            bot.send_message(user_id, "Количество участников должно быть числом")
            return

        if link.startswith("https://meet.google.com/"):
            if is_valid_google_meet_link(link):
                process_google_meet_link(link, max_participants)
            else:
                bot.send_message(user_id, "Ссылка Google Meet не валидна")
        else:
            bot.send_message(user_id, "Ссылка не распознана")
    else:
        bot.send_message(user_id, "Неизвестная команда")

