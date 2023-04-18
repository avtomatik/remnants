#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 12:32:17 2022

@author: Alexander Mikhailov
"""


from remnants.src.sql import (get_data_frame_mongo, get_psql_cursor,
                              get_sqlite3_cursor)

cursor = get_psql_cursor()
print(dir(cursor))

cursor = get_sqlite3_cursor()
print(dir(cursor))

cursor = get_data_frame_mongo()
print(dir(cursor))
