from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message):
    bot.send_message(message.chat.id, f'Hi, {message.from_user.first_name} {message.from_user.last_name}, поговорим?' )



