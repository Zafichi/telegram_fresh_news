import telebot
import os
import sqlite3
from fresh_news import get_all_users, get_all_feeds

bot_token = '1299904634:AAHl6nBdR-Qkukpn365eLirT0j_JeE7cpHQ'
tb = telebot.TeleBot(bot_token)

script_dir = os.path.dirname(os.path.realpath(__file__))
db_connection = sqlite3.connect(script_dir + '/fresh_news.sqlite', check_same_thread=False)
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS users (chat_id TEXT, news_category TEXT)')


def set_news(news_url, news_title, mess):
    with db.connection:
        chat_id = mess.chat.id
        db.execute('SELECT news_category FROM users WHERE chat_id=(?)', (chat_id,))
        news_cat = db.fetchall()
        if news_cat[0][0] == 'no_feeds':
            db.execute('UPDATE users SET news_category=(?) WHERE chat_id=(?)',
                       (news_url, chat_id))
            db.connection.commit()
            tb.send_message(mess.chat.id, 'Вы успешно подписались на {}'.format(news_title))
        elif news_cat[0][0] == 'https://news.tut.by/rss/all.rss':
            db.execute('UPDATE users SET news_category=(?) WHERE chat_id=(?)',
                       (news_url, chat_id))
            db.connection.commit()
            tb.send_message(mess.chat.id, 'Вы успешно подписались на {}'.format(news_title))
        elif news_url in get_all_feeds(mess.chat.id):
            tb.send_message(mess.chat.id, 'Вы уже подписаны на {}'.format(news_title))
        else:
            db.execute('UPDATE users SET news_category=(news_category||" "||?) WHERE chat_id=(?)',
                       (news_url, chat_id))
            db.connection.commit()
            tb.send_message(mess.chat.id, 'Вы успешно подписались на {}'.format(news_title))


while True:
    try:
        @tb.message_handler(commands=['start'])
        def start_message(message):
            tb.send_message(message.chat.id, 'Здравствуйте! Если хотите подписаться на рвссылку новостей напишите "Да"')


        @tb.message_handler(content_types=['text'])
        def send_text(message):
            chat_id = str(message.chat.id)
            if message.text.lower() == 'да':
                if chat_id in get_all_users():
                    tb.send_message(message.chat.id, 'Вы уже подписаны на рассылку новостей.')
                else:
                    db.execute('INSERT INTO users VALUES (?, ?)', (chat_id, "no_feeds"))
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
                    Чтобы сбросить все подписки напишите "/reset".''')

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
                Чтобы сбросить все подписки напишите "/reset".''')

            elif message.text.lower() == '1':
                with db.connection:
                    chat_id = message.chat.id
                    db.execute('SELECT news_category FROM users WHERE chat_id=(?)', (chat_id,))
                    news_cat = db.fetchall()
                    if news_cat[0][0] == 'no_feeds':
                        db.execute('UPDATE users SET news_category=(?) WHERE chat_id=(?)',
                                   ('https://news.tut.by/rss/all.rss', chat_id))
                        db.connection.commit()
                        tb.send_message(message.chat.id, 'Вы успешно подписались на все категории новостей.')
                    elif news_cat[0][0] == 'https://news.tut.by/rss/all.rss':
                        tb.send_message(message.chat.id, 'Вы уже подписаны на эту категорию новостей.')
                    else:
                        tb.send_message(message.chat.id,
                                        '''Вы уже подписаны на другую категорию(-и) новостей.Напишите "/да" если вы хотете 
                                        подписаться на все категории или выберете другую категорию новостей''')
            elif message.text.lower() == '/да':
                db.execute('UPDATE users SET news_category=(?) WHERE chat_id=(?)',
                           ('https://news.tut.by/rss/all.rss', chat_id))
                db.connection.commit()
                tb.send_message(message.chat.id, 'Вы успешно подписались на все категории новостей.')

            elif message.text.lower() == '2':
                set_news('https://news.tut.by/rss/index.rss', 'главные новости недели.', message)

            elif message.text.lower() == '3':
                set_news('https://news.tut.by/rss/economics.rss', 'деньги и власть.', message)

            elif message.text.lower() == '4':
                set_news('https://news.tut.by/rss/society.rss', 'общество.', message)

            elif message.text.lower() == '5':
                set_news('https://news.tut.by/rss/world.rss', '"в мире".', message)

            elif message.text.lower() == '6':
                set_news('https://news.tut.by/rss/culture.rss', 'кругозор.', message)

            elif message.text.lower() == '7':
                set_news('https://news.tut.by/rss/accidents.rss', 'проишествия.', message)

            elif message.text.lower() == '8':
                set_news('https://news.tut.by/rss/finance.rss', 'финансы.', message)

            elif message.text.lower() == '9':
                set_news('https://news.tut.by/rss/realty.rss', 'недвижимость.', message)

            elif message.text.lower() == '10':
                set_news('https://news.tut.by/rss/sport.rss', 'спорт.', message)

            elif message.text.lower() == '11':
                set_news('https://news.tut.by/rss/health.rss', 'здоровье.', message)

            elif message.text.lower() == '12':
                set_news('https://news.tut.by/rss/auto.rss', 'авто.', message)

            elif message.text.lower() == '13':
                set_news('https://news.tut.by/rss/lady.rss', 'леди.', message)

            elif message.text.lower() == '14':
                set_news('https://news.tut.by/rss/it.rss', '42.', message)

            elif message.text.lower() == '15':
                set_news('https://news.tut.by/rss/afisha.rss', 'афишу.', message)

            elif message.text.lower() == '16':
                set_news('https://news.tut.by/rss/popcorn.rss', 'попкорн.', message)

            elif message.text.lower() == '17':
                set_news('https://news.tut.by/rss/press.rss', 'новости компаний.', message)

            elif message.text.lower() == '/reset':
                db.execute('UPDATE users SET news_category=(?) WHERE chat_id=(?)',
                           ('no_feeds', chat_id))
                db.connection.commit()
                tb.send_message(message.chat.id, 'Вы успешно отписались от всех подписок.')

            # elif message.text.lower() == '-1':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от всех категорий новостей.')
            # elif message.text.lower() == '-2':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от главных новостей недели.')
            # elif message.text.lower() == '-3':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от деньг и власти.')
            # elif message.text.lower() == '-4':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от общества.')
            # elif message.text.lower() == '-5':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от "в мире".')
            # elif message.text.lower() == '-6':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от кругозора.')
            # elif message.text.lower() == '-7':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от проишествий.')
            # elif message.text.lower() == '-8':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от финансов.')
            # elif message.text.lower() == '-9':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от недвижимости.')
            # elif message.text.lower() == '-10':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от спорта.')
            # elif message.text.lower() == '-11':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от здоровья.')
            # elif message.text.lower() == '-12':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от авто.')
            # elif message.text.lower() == '-13':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от леди.')
            # elif message.text.lower() == '-14':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от 42.')
            # elif message.text.lower() == '-15':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от афиши.')
            # elif message.text.lower() == '-16':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от попкорна.')
            # elif message.text.lower() == '-17':
            #     tb.send_message(message.chat.id, 'Вы успешно отписались от новостей компаний.')
            else:
                tb.send_message(message.chat.id, 'Напишите "/help"')


        tb.infinity_polling()
    except telebot.apihelper.ApiException:
        continue
