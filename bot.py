import telebot
from telebot import types
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Замените следующие переменные своими данными
YOUR_BOT_TOKEN = '6803844464:AAGpSitsGHYZwhNn0F8zqqHpu5vrraY0f7g'
EMAIL_ADDRESS = 'havofilessending@yandex.ru'  # Ваша электронная почта
EMAIL_PASSWORD = 'tqiswyevjwxdlrgs'  # Пароль от вашей электронной почты
SMTP_SERVER = 'smtp.yandex.com'  # Адрес вашего SMTP-сервера
SMTP_PORT = 587  # Порт SMTP-сервера

bot = telebot.TeleBot(YOUR_BOT_TOKEN)

# Словарь для сохранения данных пользователей
user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("O'zbekcha", callback_data="O'zbekcha")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Русский", callback_data="Русский")
    markup.row(btn2)
    bot.send_message(message.chat.id, 'Выберите язык:', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("O'zbekcha", callback_data="O'zbekcha")
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton("Русский", callback_data="Русский")
    markup.row(btn2)
    bot.send_message(message.chat.id, 'Выберите язык:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def on_click(call):
    if call.data == "O'zbekcha":
        send_uzbek_message(call.message)
    elif call.data == "Русский":
        send_russian_message(call.message)

def send_uzbek_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = types.KeyboardButton("Mening raqamimni yuborish", request_contact=True)
    markup.row(contact_button)

    bot.send_message(message.chat.id, 'Fayl skrinshot yoki hujjat yuborish uchun telefon raqamingizni yuboring. Telefon raqamini yuborish uchun "Mening raqamimni yuborish" tugmasini bosing.',
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_name_and_surname_uz)

def send_russian_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact_button = types.KeyboardButton("Отправить мой номер", request_contact=True)
    markup.row(contact_button)

    bot.send_message(message.chat.id, 'Чтобы отправить файл, скриншот или документ, поделитесь своим номером телефона. Чтобы отправить контакт, нажмите кнопку "Отправить контакт"',
                     reply_markup=markup)
    bot.register_next_step_handler(message, get_name_and_surname_ru)

def get_name_and_surname_ru(message):
    chat_id = message.chat.id

    if message.contact:
        user_data[chat_id] = {'phone_number': message.contact.phone_number}
        bot.send_message(chat_id, 'Напишите ваше имя и фамилию:')
        bot.register_next_step_handler(message, save_name_and_surname_ru)
    else:
        bot.send_message(chat_id, 'Что-то пошло не так. Пожалуйста, используйте кнопку "Отправить контакт".')
        # Повторный запрос контакта
        send_russian_message(message)

def get_name_and_surname_uz(message):
    chat_id = message.chat.id

    if message.contact:
        user_data[chat_id] = {'phone_number': message.contact.phone_number}
        bot.send_message(chat_id, 'Ismingiz va familiyangizni yozing:')
        bot.register_next_step_handler(message, save_name_and_surname_uz)
    else:
        bot.send_message(chat_id, "Qandaydir xatolik yuz berdi. Iltimos, Mening raqamimni yuborish tugmasidan foydalaning")
        # Повторный запрос контакта
        send_uzbek_message(message)


def save_name_and_surname_ru(message):
    chat_id = message.chat.id

    if message.text:
        # Используем разделитель (например, пробел) для разбиения на имя и фамилию
        name_and_surname = message.text.split(' ', 1)

        if len(name_and_surname) == 2:
            user_data[chat_id]['name'] = name_and_surname[0]
            user_data[chat_id]['surname'] = name_and_surname[1]
            # bot.send_message(chat_id, f'Имя и фамилия сохранены: {name_and_surname[0]} {name_and_surname[1]}')
            bot.send_message(chat_id, 'Отправьте файл, скриншот или документ, который вы хотите передать в AVO')
            bot.register_next_step_handler(message, handle_file_ru)
        else:
            bot.send_message(chat_id, 'Вы должны ввести и имя, и фамилию в одном сообщении, разделенные пробелом.')
            # Повторный запрос имени и фамилии
            bot.send_message(chat_id, 'Напишите ваше имя и фамилию:')
            bot.register_next_step_handler(message, save_name_and_surname_ru)
    else:
        bot.send_message(chat_id,
                         'Вы не ввели ни имя, ни фамилию. Пожалуйста, напишите ваше имя и фамилию в одном сообщении.')
        # Повторный запрос имени и фамилии
        bot.send_message(chat_id, 'Напишите ваше имя и фамилию:')
        bot.register_next_step_handler(message, save_name_and_surname_ru)

def save_name_and_surname_uz(message):
    chat_id = message.chat.id

    if message.text:
        # Используем разделитель (например, пробел) для разбиения на имя и фамилию
        name_and_surname = message.text.split(' ', 1)

        if len(name_and_surname) == 2:
            user_data[chat_id]['name'] = name_and_surname[0]
            user_data[chat_id]['surname'] = name_and_surname[1]
            # bot.send_message(chat_id, f'Имя и фамилия сохранены: {name_and_surname[0]} {name_and_surname[1]}')
            bot.send_message(chat_id, "AVOga yubormoqchi bo'lgan fayl, skrinshot yoki hujjatingizni biriktiring.")
            bot.register_next_step_handler(message, handle_file_uz)
        else:
            bot.send_message(chat_id, "Siz bir habarning o'zida Familiya va Ismingizni  kiritshingiz kerak bo'ladi")
            # Повторный запрос имени и фамилии
            bot.send_message(chat_id, 'Ismingiz va familiyangizni yozing')
            bot.register_next_step_handler(message, save_name_and_surname_uz)
    else:
        bot.send_message(chat_id,
                         "Siz ism yoki familiya kiritmagansiz. Iltimos, bitta xabarda ismingiz va familiyangizni yozing.")
        # Повторный запрос имени и фамилии
        bot.send_message(chat_id, 'Ismingiz va familiyangizni yozing')
        bot.register_next_step_handler(message, save_name_and_surname_uz)

def handle_file_ru(message):
    chat_id = message.chat.id

    if message.photo:
        # Если отправлено изображение
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # Сохраняем изображение
        file_path = f'{file_id}.jpg'
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(chat_id, 'Спасибо, ваше изображение принято!')
        # Отправляем данные и файл на почту
        send_email_ru(chat_id, user_data[chat_id], file_path)
    elif message.video:
        # Если отправлено видео
        file_id = message.video.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # Сохраняем видео
        file_path = f'{file_id}.mp4'
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(chat_id, 'Спасибо, ваше видео принято!')
        # Отправляем данные и файл на почту
        send_email_ru(chat_id, user_data[chat_id], file_path)
    else:
        bot.send_message(chat_id, 'Формат файла не поддерживается. Пожалуйста, отправьте изображение или видео.')

def handle_file_uz(message):
    chat_id = message.chat.id

    if message.photo:
        # Если отправлено изображение
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # Сохраняем изображение
        file_path = f'{file_id}.jpg'
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(chat_id, 'Rasmingiz uchun rahmat qabul qilindi!')
        # Отправляем данные и файл на почту
        send_email_uz(chat_id, user_data[chat_id], file_path)
    elif message.video:
        # Если отправлено видео
        file_id = message.video.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # Сохраняем видео
        file_path = f'{file_id}.mp4'
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(chat_id, 'Rahmat, video qabul qilindi!')
        # Отправляем данные и файл на почту
        send_email(chat_id, user_data[chat_id], file_path)
    else:
        bot.send_message(chat_id, "Fayl formati qo'llab-quvvatlanmadi! Iltimos rasm yoki video yuboring.")

def send_email_ru(chat_id, user_info, file_path):
    to_email = 'saliboyev@avo.uz'  # Замените на адрес назначения

    subject = f'Новый файл от {user_info["name"]} {user_info["surname"]}'
    body = f'Номер телефона: {user_info["phone_number"]}\nИмя: {user_info["name"]}\nФамилия: {user_info["surname"]}'

    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Прикрепляем файл
    if os.path.exists(file_path):
        attachment = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file_path}')
        message.attach(part)

        # Отправляем письмо
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, message.as_string())

        bot.send_message(chat_id, 'Файл успешно отправлен в AVO!')
    else:
        bot.send_message(chat_id, 'Файл не найден. Пожалуйста, повторите отправку')
        # Возможно, следует добавить обработку ошибок для обработки иных ситуаций, например, если файл не существует

def send_email_uz(chat_id, user_info, file_path):
    to_email = 'saliboyev@avo.uz'  # Замените на адрес назначения

    subject = f'Новый файл от {user_info["name"]} {user_info["surname"]}'
    body = f'Номер телефона: {user_info["phone_number"]}\nИмя: {user_info["name"]}\nФамилия: {user_info["surname"]}'

    message = MIMEMultipart()
    message['From'] = EMAIL_ADDRESS
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Прикрепляем файл
    if os.path.exists(file_path):
        attachment = open(file_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {file_path}')
        message.attach(part)

        # Отправляем письмо
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, message.as_string())

        bot.send_message(chat_id, 'Fayl AVOga muvaffaqiyatli yuborildi!')
    else:
        bot.send_message(chat_id, 'Fayl topilmadi! Iltimos qayta yuboring')
        # Возможно, следует добавить обработку ошибок для обработки иных ситуаций, например, если файл не существует
#
# def restart_bot_ru(message):
#     bot.send_message(message.chat.id, 'Бот будет перезапущен')
#     # Возможно, вы захотите добавить какие-то дополнительные действия перед перезапуском
#     bot.stop_polling()
#     bot.polling(none_stop=True)
#
# def restart_bot_uz(message):
#     bot.send_message(message.chat.id, 'Bot qayta ishga tushiriladi')
#     # Возможно, вы захотите добавить какие-то дополнительные действия перед перезапуском
#     bot.stop_polling()
#     bot.polling(none_stop=True)
#
# def handle_send_more_button_ru(message):
#     chat_id = message.chat.id
#     if message.text == "Перезапустить бота":
#         restart_bot(message)
#     else:
#         # Либо обрабатываем другие варианты
#         bot.send_message(chat_id, 'Пожалуйста, воспользуйтесь кнопками для взаимодействия с ботом.')
#
# def handle_send_more_button_uz(message):
#     chat_id = message.chat.id
#     if message.text == "Botni qayta ishga tushiring":
#         rstart_bot(message)
#     else:
#         # Либо обрабатываем другие варианты
#         bot.send_message(chat_id, 'Iltimos, bot bilan ishlashni davom ettirish uchun tugmalardan foydalaning.')

if __name__ == "__main__":
    bot.polling(none_stop=True)
