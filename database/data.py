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



# def call_request(message, update: Update, context: CallbackContext) -> None:
#     if message.text == 'yes':
#         keyboard = [[types.InlineKeyboardButton("Создать звонок в Google Meet", callback_data='create_meet')]]
#         reply_markup = types.InlineKeyboardMarkup(keyboard)
#         update.message.reply_text('Выберите действие:', reply_markup=reply_markup)
#     else:
#         bot.reply_to(message, 'отдохни')
#
# def button(update: Update, context: CallbackContext) -> None:
#     query = update.callback_query
#     query.answer()
#
#     if query.data == 'create_meet':
#         # Тут должен быть код, который использует Google Meet API
#         # для создания нового звонка. Мы предполагаем, что результатом
#         # является URL нового звонка
#         # meet_url = create_meet()
#         query.edit_message_text(text=f"URL вашего звонка в Google Meet: {meet_url}")
# # при отправке команды /yes предоставляет пользователю кнопку "Создать звонок в Google Meet".
# # Когда пользователь нажимает эту кнопку, бот использует API Google Meet (предполагаемо)
# # для создания нового звонка и отправляет URL этого звонка обратно пользователю.
#
# #selenium
# def main() -> None:
#     updater = Updater("TOKEN", use_context=True)
#     dispatcher = updater.dispatcher
#     dispatcher.add_handler(CommandHandler("start", call_request))
#     dispatcher.add_handler(CallbackQueryHandler(button))
#     updater.start_polling()
#     updater.idle()

def read_file_request():
    """
    Функция для чтения запроса из файла
    :return:
    """
    with open("transcribe.txt", "r", encoding="utf-8") as file:
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


# def call_request(message):
#     response = openai.Completion.create(
#         prompt=message,
#         engine='text-davinci-003',
#         max_tokens=4000,
#         temperature=0.7,
#         n=1,
#         stop=None,
#     )
#
#
#     if response and response.choices:  # если есть ответ и есть варианты ответов(n=1)
#         reply = response.choices[0].text.strip()  # пробелы обрезаем
#         #reply = response['choices'][0]['message']['content']
#     else:
#         reply = 'smth went wrong'
#     bot.send_message(message.chat.id, reply)
#     #return response