import os

import telebot
import handler
from telebot import types

bot = telebot.TeleBot('6161654113:AAGpf8y3fKVrNDlDR2hMukAGJoo952KDYeQ')


@bot.message_handler(commands=['start'])
def start(message):
    """Приветствие пользователя"""
    bot.send_message(message.from_user.id, 'Лучший помощник начинающего '
                                           'python программиста '
                                           'приветствует вас. Моя задача - '
                                           'сделать ваш код более читаемым '
                                           'для других программистов и '
                                           'обнаружить ошибки в нём.')
    main(message)


@bot.message_handler(commands=['actions'])
def main(message):
    """Представление команд"""
    # создание кнопок в мессенджере пользователя
    markup = types.ReplyKeyboardMarkup()
    button1 = types.KeyboardButton('Проверить')
    button2 = types.KeyboardButton('Исправить')
    markup.add(button1, button2)
    bot.send_message(message.from_user.id, 'Выберите то, что я должен сделать '
                                           'с вашим кодом, нажав на '
                                           'соответствующую кнопку.',
                     reply_markup=markup)


action = None


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Получение сообщений от пользователя и соответствующие этим
    сообщениям действия"""
    global action

    if message.text == 'Проверить':
        bot.send_message(message.from_user.id, 'Отлично! Пожалуйста, '
                                               'пришлите ваш код в формате '
                                               'python файла, чтобы я мог его '
                                               'проверить.')
        # Установив action в значение 'check', бот будет ожидать следующего
        # ввода - код от пользователя, который необходимо проверить.
        action = 'check'
    elif message.text == 'Исправить':
        bot.send_message(message.from_user.id, 'Отлично! Пожалуйста, '
                                               'пришлите ваш код в формате '
                                               'python файла, чтобы я мог '
                                               'исправить его оформление и '
                                               'сделать более читаемым для '
                                               'других.')
        # Установив action в значение 'change', бот будет ожидать следующего
        # ввода - код от пользователя, который необходимо исправить.
        action = 'change'
    elif 'спасибо' in message.text.lower():
        # Бот отвечает на благодарность пользователя.
        bot.send_message(message.from_user.id, 'Обращайтесь ;)')


@bot.message_handler(content_types=['document'])
def get_file_messages(message):
    """Получение файлов от пользователя и их проверка/изменение."""
    try:
        # Загрузка файла пользователя
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Запись из файла в code.py
        src = os.getcwd() + '\\code.py'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        global action
        if action == 'check':
            # Процесс проверки
            handler_output = handler.process()
            # Проверка на количество ошибок
            if len(handler_output) == 0:
                # Ошибок нет - бот поздравляет пользователя
                bot.send_message(message.from_user.id, 'Ого, да тут ни одной '
                                                       'ошибки! Так держать!')
            else:
                # Ошибки есть - бот выводит информацию о них
                result = map(lambda x: x.report(), handler_output)
                result = '\n'.join(result)
                bot.send_message(message.from_user.id, result)
            action = None
        elif action == 'change':
            # Процесс правки.
            handler.corrections()

            # Читает результат правки из файла.
            with open('code.py', 'r') as file:
                chat_id = message.chat.id
                # Присылает результат пользователю.
                bot.send_document(chat_id, file)
            action = None
    except Exception as e:
        bot.reply_to(message, str(e))


bot.polling(none_stop=True, interval=0)
