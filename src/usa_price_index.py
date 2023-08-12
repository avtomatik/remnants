#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 14:02:58 2023

@author: green-machine
"""

import matplotlib.pyplot as plt
from core.classes import Dataset
from core.funcs import stockpile

# =============================================================================
# usa_cobb_douglas0010.py
# =============================================================================
SERIES_IDS = ['J0149', 'P0107', 'P0110']

SERIES_IDS = enlist_series_ids(
    ['CDT2S1'], Dataset.USA_COBB_DOUGLAS
) + enlist_series_ids(
    SERIES_IDS, Dataset.USCB
)

YEAR_BASE = 1958

df = stockpile(SERIES_IDS)

SERIES_IDS = ['P0107', 'P0110']
df.loc[:, SERIES_IDS] = df.loc[:, SERIES_IDS].mul(1000)

df['price_index'] = df.loc[:, 'P0107'].div(df.loc[:, 'P0110'])

LABEL = ['CDT2S1', 'J0149', '$1000 \\times P107$']

plt.figure(1)
plt.plot(df.iloc[:, range(3)], label=LABEL)
plt.title('Annual Increase of Fixed Assets in Terms of Cost Price')
plt.xlabel('Period')
plt.ylabel('Millions, USD')
plt.legend()
plt.grid()

plt.figure(2)
plt.plot(df.iloc[:, -1], label='Implicit Price Index')
plt.title(f'Price Index, {YEAR_BASE}=100')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()
plt.show()
