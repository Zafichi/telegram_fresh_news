import sqlite3
import feedparser
import os
import telebot
import sys

bot_token = '1299904634:AAHl6nBdR-Qkukpn365eLirT0j_JeE7cpHQ'
tb = telebot.TeleBot(bot_token)

# feedss = [
#     'https://news.tut.by/rss/all.rss'
# ]

script_dir = os.path.dirname(os.path.realpath(__file__))
db_connection = sqlite3.connect(script_dir + '/fresh_news.sqlite', check_same_thread=False)
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS fresh_news (title TEXT, date TEXT, link TEXT)')
db.execute('CREATE TABLE IF NOT EXISTS users (chat_id TEXT, news_category TEXT)')


def get_all_users():
    with db.connection:
        db.execute('SELECT chat_id FROM users')
        all_users = db.fetchall()
        lst_of_users = []
        for i in all_users:
            lst_of_users.append(i[0])
    return lst_of_users


# def spin_users():
#     for i in get_all_users():
#         print(i)
#     return i


def article_is_not_db(article_date, article_link):
    db.execute('SELECT * from fresh_news WHERE date=? AND link=?', (article_date, article_link))
    if not db.fetchall():
        return True
    else:
        return False


def add_article_to_db(article_title, article_date, article_link):
    db.execute('INSERT INTO fresh_news VALUES (?,?,?)', (article_title, article_date, article_link))
    db_connection.commit()


def bot_send_text(bot_message):
    for i in get_all_users():
        try:
            chat_id = i
            tb.send_message(chat_id, bot_message)
        except telebot.apihelper.ApiException:
            db.execute('DELETE FROM users WHERE chat_id = (?)', (i,))
            db_connection.commit()


def read_article_feed(feed):
    feed = feedparser.parse(feed)
    for article in feed['entries']:
        if article_is_not_db(article['published'], article['link']):
            add_article_to_db(article['title'], article['published'], article['link'])
            bot_send_text(article['title'] + ',' + article['link'])
    sys.exit()


def get_all_feeds():
    with db.connection:
        for i in get_all_users():
            db.execute('SELECT news_category FROM users WHERE chat_id=(?)', (i,))
            all_feeds = db.fetchall()
            print(all_feeds)
            for j in all_feeds:
                lst_of_feeds = j[0].split(' ')
            print(lst_of_feeds)
        return lst_of_feeds


def spin_feeds():
    for i in get_all_feeds():
        read_article_feed(i)


if __name__ == '__main__':
    # get_all_feeds()
    get_all_users()
    # spin_users()
    spin_feeds()
    tb.polling()
    db_connection.close()

