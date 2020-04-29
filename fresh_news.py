import feedparser
import psycopg2
import requests
import telebot
import time

bot_token = ''

connection = psycopg2.connect(
  database="d6a17hvofd05vd",
  user="cfvdvpggurdcyc",
  password="",
  host="ec2-46-137-156-205.eu-west-1.compute.amazonaws.com",
  port="5432"
)
cur = connection.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS fresh_news '
            '(id SERIAL NOT NULL PRIMARY KEY NOT NULL ,title TEXT, date TEXT, link TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS users (chat_id INTEGER, news_category TEXT)')


def article_is_not_db(article_date, article_link):
    cur.execute('SELECT * from fresh_news WHERE date=%s AND link=%s', (article_date, article_link))
    if not cur.fetchall():
        return True
    else:
        return False


def add_article_to_db(article_title, article_date, article_link):
    cur.execute('INSERT INTO fresh_news(title, date, link) VALUES (%s,%s,%s)',
                (article_title, article_date, article_link))
    connection.commit()


def bot_send_text(bot_message, user_chat_id):
    try:
        requests.get('https://api.telegram.org/bot{}/sendMessage'.format(bot_token), params=dict(
            chat_id=user_chat_id,
            text=bot_message))
    except telebot.apihelper.ApiException:
        cur.execute('DELETE FROM users WHERE chat_id = (%s)', (user_chat_id,))
        connection.commit()


def read_article_feed(feed):
    feed = feedparser.parse(feed)
    for article in feed['entries']:
        url = (article['title_detail']['base'])
        if article_is_not_db(article['published'], article['link']):
            add_article_to_db(article['title'], article['published'], article['link'])
            for i in get_all_users():
                cur.execute('SELECT news_category FROM users WHERE chat_id=(%s)', (i,))
                user_feeds = cur.fetchall()
                lst_of_user_feeds = []
                for j in user_feeds:
                    lst_of_user_feeds = j[0].split(' ')
                if url in lst_of_user_feeds:
                    bot_send_text(article['title'] + ',' + article['link'], i)


def get_all_users():
    with connection:
        cur.execute('SELECT chat_id FROM users')
        all_users = cur.fetchall()
        lst_of_users = []
        for i in all_users:
            lst_of_users.append(i[0])
    return lst_of_users


def get_all_feeds(user_chat_id):
    with connection:
        cur.execute('SELECT news_category FROM users WHERE chat_id=(%s)', (user_chat_id,))
        all_feeds = cur.fetchall()
        for j in all_feeds:
            lst_of_feeds = j[0].split(' ')
        for j in lst_of_feeds:
            read_article_feed(j)
    return lst_of_feeds


def spin_feeds():
    for i in get_all_users():
        get_all_feeds(i)


if __name__ == '__main__':
    while True:
        spin_feeds()
        time.sleep(60)
