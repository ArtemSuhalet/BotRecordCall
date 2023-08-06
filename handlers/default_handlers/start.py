from telebot import types

from telebot.types import Message
from loader import bot
from database import data

@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_message(message.chat.id, f'Hi, {message.from_user.first_name} {message.from_user.last_name}, поговорим?' )

    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # yes = types.KeyboardButton('yes')
    # no = types.KeyboardButton('no')
    # markup.row(yes, no)
    # msg = bot.send_message(message.from_user.id, 'if are u ready, press YES and lets go!!!', reply_markup=markup)
    # bot.register_next_step_handler(msg, data.call_request)


