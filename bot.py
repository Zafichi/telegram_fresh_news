import telebot
import os
import sqlite3
from fresh_news import get_all_users

bot_token = '1299904634:AAHl6nBdR-Qkukpn365eLirT0j_JeE7cpHQ'
tb = telebot.TeleBot(bot_token)

script_dir = os.path.dirname(os.path.realpath(__file__))
db_connection = sqlite3.connect(script_dir + '/fresh_news.sqlite', check_same_thread=False)
db = db_connection.cursor()


@tb.message_handler(commands=['start'])
def start_message(message):
    tb.send_message(message.chat.id, 'Здравствуйте! Если хотите подписаться на рвссылку новостей напишите "да"')


@tb.message_handler(content_types=['text'])
def send_text(message):
    chat_id = str(message.chat.id)
    if message.text.lower() == 'да':
        if chat_id in get_all_users():
            tb.send_message(message.chat.id, 'Вы уже подписаны на рассылку новостей.')
            pass
        else:
            db.execute('INSERT INTO users VALUES (?)', (chat_id,))
            db.connection.commit()
            tb.send_message(message.chat.id, 'Вы подписались на рассылку новостей.')


tb.polling(none_stop=True)
