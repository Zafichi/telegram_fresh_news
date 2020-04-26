import telebot
import os
import sqlite3
import feedparser
from fresh_news import get_all_users

bot_token = '1299904634:AAHl6nBdR-Qkukpn365eLirT0j_JeE7cpHQ'
tb = telebot.TeleBot(bot_token)

script_dir = os.path.dirname(os.path.realpath(__file__))
db_connection = sqlite3.connect(script_dir + '/fresh_news.sqlite', check_same_thread=False)
db = db_connection.cursor()

# with cur.connection:
#     cur.execute('SELECT news_category FROM users WHERE chat_id=537131447')
#     all_feeds = cur.fetchall()
#     print(all_feeds)
#     for i in all_feeds:
#         feeds = i[0].split(' ')
#     print(feeds)


# with cur.connection:
#     cur.execute('SELECT chat_id FROM users')
#     all_users = cur.fetchall()
#     lst_of_users = []
#     for i in all_users:
#         lst_of_users.append(i[0])
#     print(lst_of_users)
#
#
# with cur.connection:
#     chat_id = 537131447
#     cur.execute('SELECT news_category FROM users WHERE chat_id=(?)', (chat_id,))
#     news_cat = cur.fetchall()
#     print(news_cat[0])
#     print(news_cat[0][0])


feed = feedparser.parse(
    ['https://news.tut.by/rss/economics.rss', 'https://news.tut.by/rss/sport.rss', 'https://news.tut.by/rss/auto.rss',
     'https://news.tut.by/rss/health.rss', 'https://news.tut.by/rss/afisha.rss'])
print(feed['entries'])
for article in feed['entries']:
    print(article['link'])
