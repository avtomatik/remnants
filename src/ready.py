#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 20:48:46 2023

@author: green-machine
"""

import os

from funcs import stockpile_usa_hist

if __name__ == '__main__':
    PATH = '/media/green-machine/KINGSTON'
    SERIES_IDS = {'J0149': 'dataset_uscb.zip'}

    os.chdir(PATH)

    df = stockpile_usa_hist(SERIES_IDS)
    print(df)
    df = df.iloc[:, :-1]
    print(df)
