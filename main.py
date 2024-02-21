import telebot
from telebot import types

bot = telebot.TeleBot('6891304148:AAGn81BdvXxH2sFluZWyz5B07yA89vEm0gg')

phone_numbers = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("O'zbekcha", callback_data="O'zbekcha")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Русский", callback_data="Русский")
    markup.row(btn2)
    bot.send_message(message.chat.id,'Выберите язык:', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

@bot.callback_query_handler(func=lambda call: True)
def on_click(call):
    if call.data == "O'zbekcha":
        send_uzbek_message(call.message)
    elif call.data == "Русский":
        send_russian_message(call.message)

def send_uzbek_message(message):
    bot.send_message(message.chat.id, 'Fayl, skrinshot yoki hujjat yuborish uchun telefon raqamingizni yuboring')
    bot.register_next_step_handler(message, on_click)

def send_russian_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = types.KeyboardButton("Отправить контакт", request_contact=True)
    markup.row(contact_button)

    bot.send_message(message.chat.id, 'Чтобы отправить контакт, нажмите кнопку "Отправить контакт"', reply_markup=markup)


# Обработка контактов
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    chat_id = message.chat.id
    phone_numbers[chat_id] = message.contact.phone_number
    bot.send_message(chat_id, f'Номер телефона сохранен: {message.contact.phone_number}')


# Запуск бота

# def on_click(message):
#     if message.text == "O'zbekcha":
#         bot.send_message(message.chat.id, 'Fayl, skrinshot yoki hujjat yuborish uchun telefon raqamingizni yuboring')
#     elif message.text == "Русский":
#         bot.send_message(message.chat.id, 'Чтобы отправить файл, скриншот или документ, поделитесь своим номером телефона')
# #
# #
# #
#     # if message.text == "O'zbekcha":
#     #     bot.send_message(message.chat.id, 'Fayl, skrinshot yoki hujjat yuborish uchun telefon raqamingizni yuboring')
#     #
#     # elif message.text == "Русский":
#     #     bot.send_message(message.chat.id, 'Чтобы отправить файл, скриншот или документ, поделитесь своим номером телефона')
#
# # @bot.callback_query_handler(func=lambda callback:True)
# # def callback_message(callback):
# #     if callback == "O'zbekcha":
# #         bot.send_message(message.chat.id, 'Fayl, skrinshot yoki hujjat yuborish uchun telefon raqamingizni yuboring')
# #
#     elif callback == "Русский":
#         bot.send_message(message.chat.id, 'Чтобы отправить файл, скриншот или документ, поделитесь своим номером телефона')
#
#     else:
#         bot.send_message(message.chat.id, 'Отправьте номер телефона')

# @bot.message_handler(content_types=['photo', 'video'])
# def get_photo(message):
#     bot.reply_to(message, 'Получили ваш файл')


bot.polling(none_stop=True)