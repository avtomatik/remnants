#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:36:47 2023

@author: green-machine
"""


import pandas as pd
from core.constants import SERIES_IDS_LAB

from thesis.src.lib.plot import plot_cobb_douglas
from thesis.src.lib.read import read_usa_frb_g17, read_usa_frb_us3
from thesis.src.lib.stockpile import stockpile_usa_bea
from thesis.src.lib.transform import transform_cobb_douglas, transform_mean

# =============================================================================
# archiveProjectUSAINTH04.py
# =============================================================================
# =============================================================================
# Data Fetch
# =============================================================================
# =============================================================================
# Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
# =============================================================================
SERIES_ID = 'CAPUTL.B50001.A'
SERIES_IDS = {
    # =========================================================================
    # Fixed Assets Series
    # =========================================================================
    'kcn31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC
    # =========================================================================
    'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    # =========================================================================
    # Real Gross Domestic Product Series: A191RX
    # =========================================================================
    'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
}

df = pd.concat(
    [
        stockpile_usa_bea(SERIES_IDS_LAB).pipe(
            transform_mean, name='bea_labor_mfg'
        ),
        stockpile_usa_bea(SERIES_IDS),
        read_usa_frb_g17().loc[:, [SERIES_ID]].dropna(axis=0)
    ],
    axis=1,
    sort=True
)
# =============================================================================
# End Data Fetch
# =============================================================================

# =============================================================================
# Year 1947
# =============================================================================
YEAR_BASE_A = 1947 - T[0]
# =============================================================================
# Year 2005
# =============================================================================
YEAR_BASE_B = 2005 - T[0]
C = df.iloc[:, 2].mul(df.iloc[YEAR_BASE_B, 3]).div(100)
C = C.div(C[YEAR_BASE_A])
L = df.iloc[:, 1].div(df.iloc[YEAR_BASE_A, 1])
P = df.iloc[:, 5].div(df.iloc[YEAR_BASE_A, 5])
# =============================================================================
# Capacity Utilization Adjustment
# =============================================================================
# P = df.iloc[:, 5].div(df.iloc[:, 6]).div(df.iloc[YEAR_BASE_A, 5]).mul(df.iloc[YEAR_BASE_A, 6])

pd.concat([C, L, P], axis=1).pipe(
    transform_cobb_douglas, YEAR_BASE_A, 83
).pipe(plot_cobb_douglas)


# =============================================================================
# projectINTH04USA.py
# =============================================================================
SERIES_ID = 'CAPUTL.B50001.A'
SERIES_IDS = {
    # =========================================================================
    # Fixed Assets Series
    # =========================================================================
    'kcn31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
}
# =============================================================================
# TODO: Continue Series
# =============================================================================
df = pd.concat(
    [
        stockpile_usa_bea(SERIES_IDS_LAB).pipe(
            transform_mean, name='bea_labor_mfg'
        ),
        stockpile_usa_bea(SERIES_IDS),
        # =========================================================================
        # Manufacturing Series: FRBIP G17 IP, AIPMA_SA_IX, 1919--2018
        # =========================================================================
        read_usa_frb_us3().loc[:, ['AIPMA_SA_IX']],
        # =========================================================================
        # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
        # =========================================================================
        read_usa_frb_g17().loc[:, [SERIES_ID]].dropna(axis=0)
    ],
    axis=1,
    sort=True
)

# =============================================================================
# Option: 1929--2013, No Capacity Utilization Adjustment
# =============================================================================
# =============================================================================
# Year 1929
# =============================================================================
YEAR_BASE_A = 1929 - T[0]
# =============================================================================
# Year 2009
# =============================================================================
YEAR_BASE_B = 2009 - T[0]
# =============================================================================
# Year 2009
# =============================================================================
C = df.iloc[:, 3].mul(df.iloc[YEAR_BASE_B, 2]).div(100)
C = C.div(C[YEAR_BASE_A])
L = df.iloc[:, 1].div(df.iloc[YEAR_BASE_A, 1])
P = df.iloc[:, 4].div(df.iloc[YEAR_BASE_A, 4])
C, L, P = transform_cobb_douglas(YEAR_BASE_A, 95, C, L, P)
# =============================================================================
# Option: 1967--2012, No Capacity Utilization Adjustment
# =============================================================================
# =============================================================================
# Year 1967
# =============================================================================
YEAR_BASE_A = 1967 - T[0]
# =============================================================================
# Year 2009
# =============================================================================
YEAR_BASE_B = 2009 - T[0]
C = df.iloc[:, 3].mul(df.iloc[YEAR_BASE_B, 2]).div(100)
C = C.div(C[YEAR_BASE_A])
L = df.iloc[:, 1].div(df.iloc[YEAR_BASE_A, 1])
P = df.iloc[:, 4].div(df.iloc[YEAR_BASE_A, 4])
C, L, P = transform_cobb_douglas(YEAR_BASE_A, 94, C, L, P)
# =============================================================================
# Option: 1967--2012, Capacity Utilization Adjustment
# =============================================================================
# =============================================================================
# Year 1967
# =============================================================================
YEAR_BASE_A = 1967 - T[0]
# =============================================================================
# Year 2009
# =============================================================================
YEAR_BASE_B = 2009 - T[0]
C = df.iloc[:, 3].mul(df.iloc[YEAR_BASE_B, 2]).div(100)
C = C.div(C[YEAR_BASE_A])
L = df.iloc[:, 1].div(df.iloc[YEAR_BASE_A, 1])
P = df.iloc[:, 4].div(df.iloc[:, 5])
# =============================================================================
# Capacity Utilization Adjustment
# =============================================================================
P = P.div(P[YEAR_BASE_A])
C, L, P = transform_cobb_douglas(YEAR_BASE_A, 94, C, L, P)
pd.concat([C, L, P], axis=1).pipe(plot_cobb_douglas)
