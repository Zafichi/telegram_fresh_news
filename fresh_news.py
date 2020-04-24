import sqlite3
import feedparser
import os
import telebot
import sys

bot_token = '1299904634:AAHl6nBdR-Qkukpn365eLirT0j_JeE7cpHQ'
tb = telebot.TeleBot(bot_token)

script_dir = os.path.dirname(os.path.realpath(__file__))
db_connection = sqlite3.connect(script_dir + '/fresh_news.sqlite', check_same_thread=False)
db = db_connection.cursor()
db.execute('CREATE TABLE IF NOT EXISTS fresh_news '
           '(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,title TEXT, date TEXT, link TEXT)')
db.execute('CREATE TABLE IF NOT EXISTS users (chat_id TEXT, news_category TEXT)')


def article_is_not_db(article_date, article_link):
    db.execute('SELECT * from fresh_news WHERE date=? AND link=?', (article_date, article_link))
    if not db.fetchall():
        return True
    else:
        return False


def add_article_to_db(article_title, article_date, article_link):
    db.execute('INSERT INTO fresh_news(title, date, link) VALUES (?,?,?)', (article_title, article_date, article_link))
    db_connection.commit()


def bot_send_text(bot_message, user_chat_id):
    try:
        tb.send_message(user_chat_id, bot_message)
    except telebot.apihelper.ApiException:
        db.execute('DELETE FROM users WHERE chat_id = (?)', (user_chat_id,))
        db.connection.commit()


def read_article_feed(feed, user_chat_id):
    feed = feedparser.parse(feed)
    for article in feed['entries']:
        if article_is_not_db(article['published'], article['link']):
            add_article_to_db(article['title'], article['published'], article['link'])
            bot_send_text(article['title'] + ',' + article['link'], user_chat_id)


def get_all_users():
    with db_connection:
        db.execute('SELECT chat_id FROM users')
        all_users = db.fetchall()
        lst_of_users = []
        for i in all_users:
            lst_of_users.append(i[0])
    return lst_of_users


def get_all_feeds(user_chat_id):
    with db.connection:
        db.execute('SELECT news_category FROM users WHERE chat_id=(?)', (user_chat_id,))
        all_feeds = db.fetchall()
        for j in all_feeds:
            lst_of_feeds = j[0].split(' ')
        for j in lst_of_feeds:
            read_article_feed(j, user_chat_id)
    return lst_of_feeds


def spin_feeds():
    for i in get_all_users():
        get_all_feeds(i)
    sys.exit()


if __name__ == '__main__':
    # get_all_users()
    spin_feeds()
    tb.polling()
    db_connection.close()

