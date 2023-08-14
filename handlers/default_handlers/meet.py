from telebot.types import Message
from loader import bot
import openai
import os
from database.data import *
from database.meet_process import *



# @bot.message_handler(commands=['meet'])
# def handle_meet_command(message):
#     user_id = message.chat.id
#
#     # Разделяем сообщение на аргументы
#     args = message.text.split()
#     if len(args) != 2:
#         bot.send_message(user_id, "Используй: /meet <ссылка>")
#         return
#
#     # Первый аргумент - команда, второй - ссылка
#     command, link = args
#
#     if command == "/meet":
#         if link.startswith("https://meet.google.com/"):
#             if is_valid_google_meet_link(link):
#                 process_google_meet_link(link)
#             else:
#                 bot.send_message(user_id, "Ссылка Google Meet не валидна")
#         else:
#             bot.send_message(user_id, "Ссылка не распознана")
#     else:
#         bot.send_message(user_id, "Неизвестная команда")
#
#
#
