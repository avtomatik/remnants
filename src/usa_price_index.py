#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 14:02:58 2023

@author: green-machine
"""

import matplotlib.pyplot as plt
from thesis.src.lib.stockpile import stockpile_usa_hist

# =============================================================================
# project_usa_cobb_douglas0010.py
# =============================================================================
SERIES_IDS = {
    'CDT2S1': 'dataset_usa_cobb-douglas.zip',
    'J0149': 'dataset_uscb.zip',
    'P0107': 'dataset_uscb.zip',
    'P0110': 'dataset_uscb.zip',
}
YEAR_BASE = 1958

df = stockpile_usa_hist(SERIES_IDS)

SERIES_IDS = ['P0107', 'P0110']
df.loc[:, SERIES_IDS] = df.loc[:, SERIES_IDS].mul(1000)

df['price_index'] = df.loc[:, 'P0110'].div(df.loc[:, 'P0107']).mul(
    df.loc[YEAR_BASE, 'P0107']).div(df.loc[YEAR_BASE, 'P0110'])

plt.figure(1)
plt.plot(df.iloc[:, range(2)], label=['CDT2S1', 'J0149'])
plt.plot(df.iloc[:, 2], label='$1000 \\times P107$')
plt.title('Annual Increase of Fixed Assets in Terms of Cost Price')
plt.xlabel('Period')
plt.ylabel('Millions, USD')
plt.legend()
plt.grid()
plt.figure(2)
plt.plot(df.iloc[:, -1], label='Implicit Price Index')
plt.xlabel('Period')
plt.ylabel('Unity')
plt.title(f'Price Index, {YEAR_BASE}=100')
plt.legend()
plt.grid()
plt.show()
