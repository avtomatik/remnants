import json
import sqlite3

import pandas.io.sql as sql
import psycopg2
import pymongo
import requests
from pandas import DataFrame


def get_psql_cursor():
    conn = psycopg2.connect(
        dbname='stickers',
        user='stickers_admin',
        password='qwerty',
        host='localhost'
    )
    # =========================================================================
    # Return Cursor
    # =========================================================================
    return conn.cursor()


def get_sqlite3_cursor():
    query = """
    CREATE TABLE test
    (
      a VARCHAR(20),
      b VARCHAR(20),
      c REAL,
      d INTEGER
      )
    ;
"""
    con = sqlite3.connect(':memory:')
    con.execute(query)
    con.commit()

    data = [
        ('Atlanta', 'Georgia', 1.25, 6),
        ('Tallahassee', 'Florida', 2.6, 3),
        ('Sacramento', 'California', 1.7, 5),
    ]
    stmt = "INSERT INTO test VALUES(?, ?, ?, ?)"
    con.executemany(stmt, data)
    con.commit()

    cursor = con.execute('select * from test')
    rows = cursor.fetchall()
    print(sql.read_sql('select * from test', con))


def get_data_frame_mongo():
    con = pymongo.MongoClient('localhost', 27017)

    tweets = con.db.tweets

    url = 'http://search.twitter.com/search.json?q=python%20pandas'
    data = json.loads(requests.get(url).text)

    for tweet in data['results']:
        tweets.save(tweet)

    cursor = tweets.find({'from_user': 'wesmckinn'})

    tweet_fields = ['created_at', 'from_user', 'id', 'text']
    result = DataFrame(list(cursor), columns=tweet_fields)
