#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:27:12 2023

@author: green-machine
"""


import pandas as pd
from lib.tools import collect_capital_combined_archived
from pandas import DataFrame

from remnants.src.constants import SERIES_IDS_LAB
from remnants.src.plot_capital_retirement import (plot_capital_acquisition,
                                                  plot_capital_retirement)

# =============================================================================
# projectCapitalAcquisitions.py
# =============================================================================
'''Project: Capital Acquisitions'''
def combine_local() -> DataFrame:
    SERIES_ID = 'CAPUTL.B50001.A'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC1
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1929--2020
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }

    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name="bea_labor_mfg"
            ),
            read_usa_frb_g17().loc[:, [SERIES_ID]]
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)


def transform_local(df: DataFrame) -> DataFrame:
    SERIES_ID = 'CAPUTL.B50001.A'
    SERIES_IDS_TO_USE = [
        'A006RC', 'A191RC', 'A191RX', 'prod_max', 'k1n31gd1es00', 'bea_labor_mfg'
    ]
    df['prod_max'] = df.loc[:, 'A191RX'].div(df.loc[:, SERIES_ID]).mul(100)
    return df.loc[:, SERIES_IDS_TO_USE]


def transform_call(df):
    # df = combine_local().pipe(transform_local)
    _df = df.dropna()
    # =========================================================================
    # Investment
    # =========================================================================
    I = _df.iloc[:, 1].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    # =========================================================================
    # Product
    # =========================================================================
    Y = _df.iloc[:, 3]
    YN = _df.iloc[:, 2]
    # =========================================================================
    # Max: Product
    # =========================================================================
    YM = _df.iloc[:, 3].div(_df.iloc[:, 4]).mul(100)
    # =========================================================================
    # Fixed Assets, End-Period, Not Adjusted
    # =========================================================================
    C = _df.iloc[:, 6].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    L = _df.iloc[:, 7]
    plot_capital_acquisition(I, Y, YN, YM, C, L)


# =============================================================================
# 1967
# =============================================================================
# start = 38
collect_capital_combined_archived().pipe(transform_call, start=38)
# =============================================================================
# Data Fetch: Run 'projectCapital.py'
# =============================================================================


kwargs = {
    'filepath_or_buffer': 'archive project CapitalAcquisitionsRetirement.csv',
    'skiprows': range(1, 23)
}
df = pd.read_csv(**kwargs)
df['period'] = df['period'].astype(int)
# =============================================================================
# capital_retirement.yaml
# =============================================================================
T = df.iloc[:, 0]
# =============================================================================
# Investment
# =============================================================================
I = df.iloc[:, 1].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
# =============================================================================
# Product
# =============================================================================
Y = df.iloc[:, 3]
YN = df.iloc[:, 2]
# =============================================================================
# Max: Product
# =============================================================================
# YM = df.iloc[:, 3].div(df.iloc[:, 4]).div(100)
# Fixed Assets, End-Period, Not Adjusted
C = df.iloc[:, 6].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
L = df.iloc[:, 7]
# =============================================================================
# C = df.iloc[:, 5].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
# =============================================================================
# =============================================================================
# L = df.iloc[:, 8]
# =============================================================================
# =============================================================================
# Replaced with
# =============================================================================
# =============================================================================
# C = df.iloc[:, 6].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
# =============================================================================
# =============================================================================
# L = df.iloc[:, 7]
# =============================================================================

plot_capital_retirement(I, Y, YN, C, L)

