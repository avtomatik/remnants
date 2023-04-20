#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:03:14 2023

@author: green-machine
"""


import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

from constants import SERIES_IDS_PRCH
from thesis.src.lib.collect import stockpile_cobb_douglas, stockpile_usa_hist
from thesis.src.lib.plot import plot_cobb_douglas
from thesis.src.lib.tools import construct_usa_hist_deflator
from thesis.src.lib.transform import (transform_cobb_douglas,
                                      transform_cobb_douglas_alt,
                                      transform_mean)

# =============================================================================
# usa_cobb_douglas0003.py
# =============================================================================


# =============================================================================
# The Revised Index of Physical Production for All Manufacturing In the United States, 1899--1926
# =============================================================================

stockpile_cobb_douglas(5).iloc[:, [0, 1, 4]].pipe(
    transform_cobb_douglas).pipe(plot_cobb_douglas)
# =============================================================================
# usa_cobb_douglas0004.py
# =============================================================================


stockpile_cobb_douglas(4).pipe(transform_cobb_douglas_alt)


# =============================================================================
# projectDataFusionUSACostIndex.py
# =============================================================================


# =============================================================================
# Combine L2, L15, E7, E23, E40, E68 & P107/P110
# =============================================================================
# =============================================================================
# Bureau of Labor Statistics: Data Not Used As It Covers Only Years of 1998--2017
# =============================================================================
# =============================================================================
# Results:
# {'L0036': 'dataset_uscb.zip'} Offset With {'E0183': 'dataset_uscb.zip'}
# {'L0038': 'dataset_uscb.zip'} Offset With {'E0184': 'dataset_uscb.zip'}
# {'L0039': 'dataset_uscb.zip'} Offset With {'E0185': 'dataset_uscb.zip'}
# {'E0052': 'dataset_uscb.zip'} Offset With {'L0002': 'dataset_uscb.zip'}
# =============================================================================

SERIES_IDS = {
    'E0007': 'dataset_uscb.zip',
    # =========================================================================
    # 'E0008': 'dataset_uscb.zip'
    # 'E0009': 'dataset_uscb.zip'
    # =========================================================================
    'E0023': 'dataset_uscb.zip',
    'E0040': 'dataset_uscb.zip',
    'E0068': 'dataset_uscb.zip',
    # =========================================================================
    # 'E0186': 'dataset_uscb.zip',
    # =========================================================================
    # =========================================================================
    # Snyder-Tucker
    # =========================================================================
    'L0001': 'dataset_uscb.zip',
    # =========================================================================
    # Warren & Pearson
    # =========================================================================
    'L0002': 'dataset_uscb.zip',
    'L0015': 'dataset_uscb.zip',
    # =========================================================================
    # 'L0037': 'dataset_uscb.zip',
    # =========================================================================
}

# =============================================================================
# pd.concat(
#     [
#         stockpile_usa_hist(SERIES_IDS).pct_change(),
#         construct_usa_hist_deflator(SERIES_IDS_PRCH)
#     ],
#     axis=1
# ).dropna(how='all').plot(grid=True)
# =============================================================================
# =============================================================================
# plt.title('Cost Index')
# plt.xlabel('Period')
# plt.ylabel('Unity')
# plt.legend()
# =============================================================================

df = pd.concat(
    [
        pd.concat(
            [
                stockpile_usa_hist(SERIES_IDS).pct_change(),
                construct_usa_hist_deflator(SERIES_IDS_PRCH)
            ],
            axis=1
        ).dropna(how='all').pipe(transform_mean, name='df_uscb'),
        construct_usa_hist_deflator(SERIES_IDS_CD)
    ],
    axis=1,
    sort=True
)

plt.figure(1)
plt.plot(df)
plt.xlabel('Period')
plt.ylabel('Price Index')
plt.title('Chart$-$Cost Index Comparison')
plt.grid()
plt.legend(['Revised Dataset', 'Cobb$-$Douglas Dataset'])
# =============================================================================
# plt.savefig('costIndexComparison.pdf', format='pdf', dpi=900)
# =============================================================================
SERIES_IDS = {
    'E0183': 'dataset_uscb.zip',
    'E0184': 'dataset_uscb.zip',
    'E0185': 'dataset_uscb.zip',
}
stockpile_usa_hist(SERIES_IDS).pct_change().dropna(how='all').plot(grid=True)
# =============================================================================
# plt.title('Cost Index')
# plt.xlabel('Period')
# plt.ylabel('Unity')
# plt.legend()
# =============================================================================

plt.figure(2)
plt.plot(ppi[205]/ppi, label='Price Index 1958=100')
plt.xlabel('Period')
plt.ylabel('Price Index')
plt.title('Chart$-$Revised Price Index')
plt.legend()
plt.grid()
plt.show()
# =============================================================================
# TODO: Compare Above with BEA k* Series
# =============================================================================


# =============================================================================
# projectUSACensus0002.py
# =============================================================================

# =============================================================================
# Census Manufacturing Fixed Assets Series
# =============================================================================
SERIES_IDS = {
    'P0107': 'dataset_uscb.zip',
    'P0108': 'dataset_uscb.zip',
    'P0109': 'dataset_uscb.zip',
    'P0110': 'dataset_uscb.zip',
    'P0111': 'dataset_uscb.zip',
    'P0112': 'dataset_uscb.zip',
    'P0113': 'dataset_uscb.zip',
    'P0114': 'dataset_uscb.zip',
    'P0115': 'dataset_uscb.zip',
    'P0116': 'dataset_uscb.zip',
    'P0117': 'dataset_uscb.zip',
    'P0118': 'dataset_uscb.zip',
    'P0119': 'dataset_uscb.zip',
    'P0120': 'dataset_uscb.zip',
    'P0121': 'dataset_uscb.zip',
    'P0122': 'dataset_uscb.zip',
}

df = stockpile_usa_hist(SERIES_IDS)
df['p110_over_p107'] = df.loc[:, 'P0110'].div(df.loc[:, 'P0107'])
df['p111_over_p108'] = df.loc[:, 'P0111'].div(df.loc[:, 'P0108'])
df['p112_over_p109'] = df.loc[:, 'P0112'].div(df.loc[:, 'P0109'])
df['x_index'] = df.loc[:, 'P0110'].div(
    df.loc[:, 'P0107']).div(df.loc[:, 'P0119'])
df['x_index'] = df['x_index'].div(df.loc[1958, 'x_index'])
# =============================================================================
# Re-Confirm Below Series
# =============================================================================

plt.figure(1)
plt.semilogy(df.iloc[:, :-4])
plt.title('TBA')
plt.xlabel('Period')
plt.ylabel('Billions, USD')
plt.grid()
plt.legend()

plt.figure(2)
plt.plot(
    df.iloc[:, -4:],
    label=[
        '$\\frac{P110}{P107}$',
        '$\\frac{P111}{P108}$',
        '$\\frac{P112}{P109}$',
        '$\\frac{P110}{P107 \\times P119}$, 1958=100'
    ]
)
plt.title('Deflators')
plt.xlabel('Period')
plt.ylabel('Unity')
plt.legend()
plt.grid()
plt.show()


# =============================================================================
# usa_cobb_douglas0009.py
# =============================================================================


def transform_plot(df: DataFrame):
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Labor
        df.iloc[:, 2]      Product
        ================== =================================
    """
    df['lab_cap_int'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['lab_product'] = df.iloc[:, 2].div(df.iloc[:, 1])
    X2 = df['lab_cap_int'].rolling(window=2, center=True).mean()
    Y2 = df['lab_product'].rolling(window=2, center=True).mean()
    Y3 = df['lab_product'].rolling(window=3, center=True).mean()
    Y4 = df['lab_product'].rolling(window=4, center=True).mean()
    df['lab_cap_int'].pipe(plot_filter_kol_zur)
    df['lab_cap_int'].pipe(plot_filter_rolling_mean)
    df['lab_cap_int'].pipe(plot_ewm)
    # =========================================================================
    # Figure 1
    # =========================================================================
    # Series 1
    # df['lab_cap_int'].pipe(plot_filter_kol_zur)
    # =========================================================================
    # Extra: 1
    # =========================================================================
    # Series 2
    # Header: Sheet1!$C$1
    # X Series: Period
    # Y Series: X @ WINDOW: 2 # <plot_filter_rolling_mean> CobbDouglas X [1:25]
    # =========================================================================
    # Extra: 2
    # =========================================================================
    # Series 3
    # Header: Sheet1!$F$1
    # X Series: Period
    # Y Series: X @ DELTA{1} # <plot_filter_kol_zur> CobbDouglas X [1:25]
    # =========================================================================
    # Extra: 3
    # =========================================================================
    # Series 4
    # Header: Sheet1!$I$1
    # X Series: Period
    # Y Series: X @ SMOOTHING (WINDOW: 5, ALPHA: 0.25) # <plot_ewm> CobbDouglas X [1:25]
    # =========================================================================
    # Extra: 4
    # =========================================================================
    # =========================================================================
    # Figure 2
    # =========================================================================
    # Series 1
    # =========================================================================
    # Header: Y
    # =========================================================================
    # X Series: Period
    # Y Series: Y
    # =========================================================================
    # Extra: 1
    # =========================================================================
    # Series 2
    # Header: Sheet2!$C$1
    # X Series: Period
    # Y Series: Y @ WINDOW: 2 # <plot_filter_rolling_mean> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 2
    # =========================================================================
    # Series 3
    # Header: Sheet2!$D$1
    # X Series: Period
    # Y Series: Y @ WINDOW: 3 # <plot_filter_rolling_mean> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 3
    # =========================================================================
    # Series 4
    # Header: Sheet2!$E$1
    # X Series: Period
    # Y Series: Y @ WINDOW: 4 # <plot_filter_rolling_mean> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 4
    # =========================================================================
    # Series 5
    # Header: Sheet2!$F$1
    # X Series: Period
    # Y Series: Y @ DELTA{1} # <plot_filter_kol_zur> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 5
    # =========================================================================
    # Series 6
    # Header: Sheet2!$G$1
    # X Series: Period
    # Y Series: Y @ DELTA{2} # <plot_filter_kol_zur> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 6
    # =========================================================================
    # Series 7
    # Header: Sheet2!$H$1
    # X Series: Period
    # Y Series: Y @ DELTA{3} # <plot_filter_kol_zur> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 7
    # =========================================================================
    # Series 8
    # Header: Sheet2!$I$1
    # X Series: Period
    # Y Series: Y @ SMOOTHING (WINDOW: 5, ALPHA: 0.25) # <plot_ewm> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 8
    # =========================================================================
    # Series 9
    # Header: Sheet2!$J$1
    # X Series: Period
    # Y Series: Y @ SMOOTHING (WINDOW: 5, ALPHA: 0.35) # <plot_ewm> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 9
    # =========================================================================
    # Series 10
    # Header: Sheet2!$K$1
    # X Series: Period
    # Y Series: Y @ SMOOTHING (WINDOW: 5, ALPHA: 0.45) # <plot_ewm> CobbDouglas Y [1:25]
    # =========================================================================
    # Extra: 10
    # =========================================================================
    plt.figure(1)
    plt.plot(df['lab_cap_int'])
    plt.plot(X2, ':')
    plt.xlabel('Period')
    plt.ylabel('Labor Capital Intensity')
    plt.grid()
    plt.figure(2)
    plt.plot(df['lab_product'])
    plt.plot(Y2, ':')
    plt.plot(Y3, ':')
    plt.plot(Y4, ':')
    plt.xlabel('Period')
    plt.ylabel('Labor Productivity')
    plt.grid()
    plt.show()


stockpile_cobb_douglas().pipe(transform_plot)

# =============================================================================
# usa_cobb_douglas0010Flow.py
# =============================================================================

SERIES_IDS = {
    'CDT2S1': 'dataset_usa_cobb-douglas.zip',
    'CDT2S3': 'dataset_usa_cobb-douglas.zip',
    'DT63AS02': 'dataset_douglas.zip',
    'J0149': 'dataset_uscb.zip',
    'J0150': 'dataset_uscb.zip',
    'J0151': 'dataset_uscb.zip',
    'P0107': 'dataset_uscb.zip',
    'P0108': 'dataset_uscb.zip',
    'P0109': 'dataset_uscb.zip',
}
YEAR_BASE = 1958

df = stockpile_usa_hist(SERIES_IDS)

SERIES_IDS = ['P0107', 'P0108', 'P0109']
df.loc[:, SERIES_IDS] = df.loc[:, SERIES_IDS].mul(1000)

LEGEND = ['CDT2S1', 'J0149', 'J0150', 'J0151']
plt.figure(1)
plt.plot(df.loc[:, LEGEND])
plt.title('Fixed Assets Increment')
plt.xlabel('Period')
plt.ylabel('Millions or Billions? Dollars')
plt.legend(LEGEND)
plt.grid()

LEGEND = ['P0107', 'P0108', 'P0109']
plt.figure(2)
plt.semilogy(df.loc[:, LEGEND])
plt.title('Fixed Assets Increment')
plt.xlabel('Period')
plt.ylabel('Millions or Billions? Dollars')
plt.legend(LEGEND)
plt.grid()

LEGEND = ['CDT2S3', 'DT63AS02']
plt.figure(3)
plt.plot(df.loc[:, LEGEND])
plt.title(f'Fixed Assets Increment, {YEAR_BASE}?=100')
plt.xlabel('Period')
plt.ylabel('Millions or Billions? Dollars')
plt.legend(LEGEND)
plt.grid()

LEGEND = ['CDT2S1', 'J0149', 'P0107']
plt.figure(4)
plt.semilogy(df.loc[:, LEGEND])
plt.title('Fixed Assets Increment, Cobb$-$Douglas, Census 1949 & 1975 Versions')
plt.xlabel('Period')
plt.ylabel('Millions or Billions? Dollars')
plt.legend(LEGEND)
plt.grid()
plt.show()
