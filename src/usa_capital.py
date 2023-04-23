#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:59:39 2023

@author: green-machine
"""


import matplotlib.pyplot as plt
from thesis.src.lib.stockpile import stockpile_usa_hist

# =============================================================================
# project_usa_cobb_douglas0006.py
# =============================================================================
# =============================================================================
# Manufacturing Fixed Assets Series Comparison
# =============================================================================
# =============================================================================
# TODO: Make More Robust Adjustment
# =============================================================================

SERIES_IDS = {
    'CDT2S1': 'dataset_usa_cobb-douglas.zip',
    'CDT2S3': 'dataset_usa_cobb-douglas.zip',
    'CDT2S4': 'dataset_usa_cobb-douglas.zip',
    'P0107': 'dataset_uscb.zip',
    'P0110': 'dataset_uscb.zip',
    'P0119': 'dataset_uscb.zip',
    # =========================================================================
    # 'Чистый основной капитал (в млн. долл., 1929 г.)'
    # =========================================================================
    'brown_0x1': 'dataset_usa_brown.zip'
}

# =============================================================================
# Package combine_usa_capital
# =============================================================================
df = stockpile_usa_hist(SERIES_IDS).truncate(before=1869)

SERIES_IDS = ['P0107', 'P0110', 'P0119']
df.loc[:, SERIES_IDS] = df.loc[:, SERIES_IDS].mul(1000)

# =============================================================================
# Nominal Fixed Assets Values, Billions of Dollars, as per Cobb-Douglas: Revised
# =============================================================================
df['nominal_cbb_dg'] = df.loc[:, 'CDT2S1'].mul(
    df.loc[:, 'CDT2S4']).div(df.loc[:, 'CDT2S3'])
df['nominal_uscb'] = df.loc[:, 'P0107'].mul(
    df.loc[:, 'P0119']).div(df.loc[:, 'P0110'])

# =============================================================================
# TODO: Insert FRBIP Data
# =============================================================================
plt.figure()
plt.plot(df.iloc[:, -3:])
# =============================================================================
# ls=['-.', '-', '-.']
# =============================================================================
plt.title('US Nominal Manufacturing Fixed Assets')
plt.xlabel('Period')
plt.ylabel('Billions of Dollars')
plt.legend()
plt.grid()
plt.show()
