#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:32:17 2022

@author: Alexander Mikhailov
"""

import psycopg2

conn = psycopg2.connect(
    dbname='stickers',
    user='stickers_admin',
    password='qwerty',
    host='localhost'
)
cursor = conn.cursor()
print(dir(cursor))
