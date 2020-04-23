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
    tb.send_message(message.chat.id, 'Здравствуйте! Если хотите подписаться на рвссылку новостей напишите "Да"')


@tb.message_handler(content_types=['text'])
def send_text(message):
    chat_id = str(message.chat.id)
    if message.text.lower() == 'да':
        if chat_id in get_all_users():
            tb.send_message(message.chat.id, 'Вы уже подписаны на рассылку новостей.')
            pass
        else:
            db.execute('INSERT INTO users VALUES (?, ?)', (chat_id, None))
            db.connection.commit()
            tb.send_message(message.chat.id,
                            '''Выберете категорию новостей на которую вы хотите подписаться.
            Напишите: 
            "1" - новости всех категорий
            "2" - главные новости недели
            "3" - деньги и власть
            "4" - общество
            "5" - в мире                                
            "6" - кругозор
            "7" - проишествия                                
            "8" - финансы
            "9" - недвижимость
            "10" - спорт
            "11" - здоровье
            "12" - авто
            "13" - леди
            "14" - 42
            "15" - афиша
            "16" - попкорн
            "17" - новости компаний
            Чтобы отписаться поставте "-" перед цифрой категории новостей.''')
    elif message.text.lower() == '/help':
        tb.send_message(message.chat.id,
                        '''Выберете категорию новостей на которую вы хотите подписаться.
        Напишите: 
        "1" - новости всех категорий
        "2" - главные новости недели
        "3" - деньги и власть
        "4" - общество
        "5" - в мире                                
        "6" - кругозор
        "7" - проишествия                                
        "8" - финансы
        "9" - недвижимость
        "10" - спорт
        "11" - здоровье
        "12" - авто
        "13" - леди
        "14" - 42
        "15" - афиша
        "16" - попкорн
        "17" - новости компаний
        Чтобы отписаться поставте "-" перед цифрой категории новостей.''')

    elif message.text.lower() == '1':
        with db.connection:
            chat_id = message.chat.id
            db.execute('SELECT news_category FROM users WHERE chat_id=(?)', (chat_id,))
            # news_cat = db.fetchall()
            db.execute('UPDATE users SET news_category=(?) WHERE chat_id=(?)',
                       ('https://news.tut.by/rss/all.rss', chat_id))
        tb.send_message(message.chat.id, 'Вы успешно подписались на все категории новостей.')
    elif message.text.lower() == '2':
        with db.connection:
            chat_id = message.chat.id
            db.execute('SELECT news_category FROM users WHERE chat_id=(?)', (chat_id,))
            # news_cat = db.fetchall()
            db.execute('UPDATE users SET news_category=(news_category||" "||?) WHERE chat_id=(?)',
                       ('https://news.tut.by/rss/index.rss', chat_id))
        tb.send_message(message.chat.id, 'Вы успешно подписались на главные новости недели.')
    elif message.text.lower() == '3':
        with db.connection:
            chat_id = message.chat.id
            db.execute('SELECT news_category FROM users WHERE chat_id=(?)', (chat_id,))
            # news_cat = db.fetchall()
            db.execute('UPDATE users SET news_category=(news_category||" "||?) WHERE chat_id=(?)',
                       ('https://news.tut.by/rss/economics.rss', chat_id))
        tb.send_message(message.chat.id, 'Вы успешно подписались на деньги и власть.')
    elif message.text.lower() == '4':
        tb.send_message(message.chat.id, 'Вы успешно подписались на общество.')
    elif message.text.lower() == '5':
        tb.send_message(message.chat.id, 'Вы успешно подписались на "в мире".')
    elif message.text.lower() == '6':
        tb.send_message(message.chat.id, 'Вы успешно подписались на кругозор.')
    elif message.text.lower() == '7':
        tb.send_message(message.chat.id, 'Вы успешно подписались на проишествия.')
    elif message.text.lower() == '8':
        tb.send_message(message.chat.id, 'Вы успешно подписались на финансы.')
    elif message.text.lower() == '9':
        tb.send_message(message.chat.id, 'Вы успешно подписались на недвижимость.')
    elif message.text.lower() == '10':
        tb.send_message(message.chat.id, 'Вы успешно подписались на спорт.')
    elif message.text.lower() == '11':
        tb.send_message(message.chat.id, 'Вы успешно подписались на здоровье.')
    elif message.text.lower() == '12':
        tb.send_message(message.chat.id, 'Вы успешно подписались на авто.')
    elif message.text.lower() == '13':
        tb.send_message(message.chat.id, 'Вы успешно подписались на леди.')
    elif message.text.lower() == '14':
        tb.send_message(message.chat.id, 'Вы успешно подписались на 42.')
    elif message.text.lower() == '15':
        tb.send_message(message.chat.id, 'Вы успешно подписались на афишу.')
    elif message.text.lower() == '16':
        tb.send_message(message.chat.id, 'Вы успешно подписались на попкорн.')
    elif message.text.lower() == '17':
        tb.send_message(message.chat.id, 'Вы успешно подписались на новости компаний.')

    elif message.text.lower() == '-1':
        tb.send_message(message.chat.id, 'Вы успешно отписались от всех категорий новостей.')
    elif message.text.lower() == '-2':
        tb.send_message(message.chat.id, 'Вы успешно отписались от главных новостей недели.')
    elif message.text.lower() == '-3':
        tb.send_message(message.chat.id, 'Вы успешно отписались от деньг и власти.')
    elif message.text.lower() == '-4':
        tb.send_message(message.chat.id, 'Вы успешно отписались от общества.')
    elif message.text.lower() == '-5':
        tb.send_message(message.chat.id, 'Вы успешно отписались от "в мире".')
    elif message.text.lower() == '-6':
        tb.send_message(message.chat.id, 'Вы успешно отписались от кругозора.')
    elif message.text.lower() == '-7':
        tb.send_message(message.chat.id, 'Вы успешно отписались от проишествий.')
    elif message.text.lower() == '-8':
        tb.send_message(message.chat.id, 'Вы успешно отписались от финансов.')
    elif message.text.lower() == '-9':
        tb.send_message(message.chat.id, 'Вы успешно отписались от недвижимости.')
    elif message.text.lower() == '-10':
        tb.send_message(message.chat.id, 'Вы успешно отписались от спорта.')
    elif message.text.lower() == '-11':
        tb.send_message(message.chat.id, 'Вы успешно отписались от здоровья.')
    elif message.text.lower() == '-12':
        tb.send_message(message.chat.id, 'Вы успешно отписались от авто.')
    elif message.text.lower() == '-13':
        tb.send_message(message.chat.id, 'Вы успешно отписались от леди.')
    elif message.text.lower() == '-14':
        tb.send_message(message.chat.id, 'Вы успешно отписались от 42.')
    elif message.text.lower() == '-15':
        tb.send_message(message.chat.id, 'Вы успешно отписались от афиши.')
    elif message.text.lower() == '-16':
        tb.send_message(message.chat.id, 'Вы успешно отписались от попкорна.')
    elif message.text.lower() == '-17':
        tb.send_message(message.chat.id, 'Вы успешно отписались от новостей компаний.')
    else:
        tb.send_message(message.chat.id, 'Напишите "/help"')


tb.infinity_polling()
