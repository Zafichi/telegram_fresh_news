import telebot
import psycopg2
from fresh_news import get_all_users, get_all_feeds

bot_token = '1299904634:AAE9Ni1mQ2FPifpzulfcXETziWB4kEKhqjw'
tb = telebot.TeleBot(bot_token)

logger = telebot.logger

connection = psycopg2.connect(
  database="d6a17hvofd05vd",
  user="cfvdvpggurdcyc",
  password="798725c679f1e5e7a362e6e57e037a7632ace5b6eac8d09167588bad5ab58131",
  host="localhost",
  port="5432"
)
cur = connection.cursor()
str_of_urls = 'https://news.tut.by/rss/index.rss https://news.tut.by/rss/economics.rss ' \
              'https://news.tut.by/rss/society.rss https://news.tut.by/rss/world.rss ' \
              'https://news.tut.by/rss/culture.rss https://news.tut.by/rss/accidents.rss ' \
              'https://news.tut.by/rss/finance.rss https://news.tut.by/rss/realty.rss ' \
              'https://news.tut.by/rss/sport.rss https://news.tut.by/rss/health.rss https://news.tut.by/rss/auto.rss ' \
              'https://news.tut.by/rss/lady.rss https://news.tut.by/rss/it.rss https://news.tut.by/rss/afisha.rss ' \
              'https://news.tut.by/rss/popcorn.rss https://news.tut.by/rss/press.rss '


def set_news(news_url, news_title, mess):
    with connection:
        chat_id = mess.chat.id
        cur.execute('SELECT news_category FROM users WHERE chat_id=(%s)', (chat_id,))
        news_cat = cur.fetchall()
        if news_cat[0][0] == 'no_feeds':
            cur.execute('UPDATE users SET news_category=(%s) WHERE chat_id=(%s)',
                        (news_url, chat_id))
            connection.commit()
            tb.send_message(mess.chat.id, 'Вы успешно подписались на {}'.format(news_title))
        elif news_cat[0][0] == str_of_urls:
            cur.execute('UPDATE users SET news_category=(%s) WHERE chat_id=(%s)',
                        (news_url, chat_id))
            connection.commit()
            tb.send_message(mess.chat.id, 'Вы успешно подписались на {}'.format(news_title))
        elif news_url in get_all_feeds(mess.chat.id):
            tb.send_message(mess.chat.id, 'Вы уже подписаны на {}'.format(news_title))
        else:
            cur.execute('UPDATE users SET news_category=format(news_category || %s) WHERE chat_id=(%s)',
                        (news_url, chat_id))
            connection.commit()
            tb.send_message(mess.chat.id, 'Вы успешно подписались на {}'.format(news_title))


@tb.message_handler(commands=['start'])
def start_message(message):
    tb.send_message(message.chat.id, 'Здравствуйте! Если хотите подписаться на рвссылку новостей напишите "Да"')


@tb.message_handler(content_types=['text'])
def send_text(message):
    chat_id = message.chat.id
    if message.text.lower() == 'да':
        if chat_id in get_all_users():
            tb.send_message(message.chat.id, 'Вы уже подписаны на рассылку новостей.')
        else:
            cur.execute("INSERT INTO users (chat_id, news_category) VALUES (%s, %s);", (chat_id, "no_feeds"))
            connection.commit()
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
        with connection:
            cur.execute('SELECT news_category FROM users WHERE chat_id=(%s)', (chat_id,))
            news_cat = cur.fetchall()
            if news_cat[0][0] == 'no_feeds':
                cur.execute('UPDATE users SET news_category=(%s) WHERE chat_id=(%s)',
                            (str_of_urls, chat_id))
                connection.commit()
                tb.send_message(message.chat.id, 'Вы успешно подписались на все категории новостей.')
            elif news_cat[0][0] == str_of_urls:
                tb.send_message(message.chat.id, 'Вы уже подписаны на эту категорию новостей.')
            else:
                tb.send_message(message.chat.id,
                                '''Вы уже подписаны на другую категорию(-и) новостей.Напишите "/да" если вы хотете 
                                подписаться на все категории или выберете другую категорию новостей''')
    elif message.text.lower() == '/да':
        cur.execute('UPDATE users SET news_category=(%s) WHERE chat_id=(%s)',
                    (str_of_urls, chat_id))
        connection.commit()
        tb.send_message(message.chat.id, 'Вы успешно подписались на все категории новостей.')

    elif message.text.lower() == '2':
        set_news('https://news.tut.by/rss/index.rss ', 'главные новости недели.', message)

    elif message.text.lower() == '3':
        set_news('https://news.tut.by/rss/economics.rss ', 'деньги и власть.', message)

    elif message.text.lower() == '4':
        set_news('https://news.tut.by/rss/society.rss ', 'общество.', message)

    elif message.text.lower() == '5':
        set_news('https://news.tut.by/rss/world.rss ', '"в мире".', message)

    elif message.text.lower() == '6':
        set_news('https://news.tut.by/rss/culture.rss ', 'кругозор.', message)

    elif message.text.lower() == '7':
        set_news('https://news.tut.by/rss/accidents.rss ', 'проишествия.', message)

    elif message.text.lower() == '8':
        set_news('https://news.tut.by/rss/finance.rss ', 'финансы.', message)

    elif message.text.lower() == '9':
        set_news('https://news.tut.by/rss/realty.rss ', 'недвижимость.', message)

    elif message.text.lower() == '10':
        set_news('https://news.tut.by/rss/sport.rss ', 'спорт.', message)

    elif message.text.lower() == '11':
        set_news('https://news.tut.by/rss/health.rss ', 'здоровье.', message)

    elif message.text.lower() == '12':
        set_news('https://news.tut.by/rss/auto.rss ', 'авто.', message)

    elif message.text.lower() == '13':
        set_news('https://news.tut.by/rss/lady.rss ', 'леди.', message)

    elif message.text.lower() == '14':
        set_news('https://news.tut.by/rss/it.rss ', '42.', message)

    elif message.text.lower() == '15':
        set_news('https://news.tut.by/rss/afisha.rss ', 'афишу.', message)

    elif message.text.lower() == '16':
        set_news('https://news.tut.by/rss/popcorn.rss ', 'попкорн.', message)

    elif message.text.lower() == '17':
        set_news('https://news.tut.by/rss/press.rss ', 'новости компаний.', message)

    elif message.text.lower() == '/reset':
        cur.execute('UPDATE users SET news_category=(%s) WHERE chat_id=(%s)',
                    ('no_feeds', chat_id))
        cur.connection.commit()
        tb.send_message(message.chat.id, 'Вы успешно отписались от всех подписок.')

    else:
        tb.send_message(message.chat.id, 'Напишите "/help"')


tb.infinity_polling(True)
