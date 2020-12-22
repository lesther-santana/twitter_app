import sqlite3

# Para crear tablas en caso de que no existan!
'''
with sqlite3.connect('tweet_data.db') as con:
    cursor = con.cursor()
    cursor.execute(
    CREATE TABLE IF NOT EXISTS TWEET_COUNTS(
	TIME text PRIMARY KEY,
	BATCH_SIZE integer,
	RETWEETS integer,
	QUOTES integer,
    REPLYS integer))
'''

# Para crear tabla de tweets

with sqlite3.connect('tweet_data.db') as con:
    cursor = con.cursor()
    cursor.execute(
    '''CREATE TABLE IF NOT EXISTS TWEETS(
	CREATED_AT text,
	ID TEXT PRIMARY KEY,
	USER_ID text,
    USER_NAME text,
    USER_SCREEN_NAME text,
    TEXT text,
    LANG text,
    HASHTAGS text,
    USER_MENTIONS text,
    SOURCE text,
    COORDS text,
    COORDS_TYPE text,
    IS_QUOTE text,
    IS_RETWEET text,
    IS_REPLY text);''')
