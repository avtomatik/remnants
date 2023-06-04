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
from remnants.src.constants import SERIES_IDS_CD
from thesis.src.lib.plot import plot_cobb_douglas
from thesis.src.lib.stockpile import stockpile_usa_hist
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
YEAR_BASE = 1899
plot_cobb_douglas(
    *combine_cobb_douglas(5).iloc[:, [0, 1, -1]].pipe(
        transform_cobb_douglas, YEAR_BASE
    ),
    get_fig_map_us_ma(YEAR_BASE)
)


# =============================================================================
# usa_cobb_douglas0004.py
# =============================================================================
YEAR_BASE = 1899
plot_cobb_douglas_alt(
    *combine_cobb_douglas(4).pipe(
        transform_cobb_douglas_alt, YEAR_BASE
    ),
    get_fig_map(YEAR_BASE)
)


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
# {'E0183' or 'L0036': 'dataset_uscb.zip'}
# {'E0184' or 'L0038': 'dataset_uscb.zip'}
# {'E0185' or 'L0039': 'dataset_uscb.zip'}
# =============================================================================
SERIES_IDS = {
    'E0007': 'dataset_uscb.zip',
    'E0008': 'dataset_uscb.zip',
    'E0009': 'dataset_uscb.zip',
    'E0023': 'dataset_uscb.zip',
    'E0040': 'dataset_uscb.zip',
    'E0068': 'dataset_uscb.zip',
    'E0183': 'dataset_uscb.zip',
    'E0184': 'dataset_uscb.zip',
    'E0185': 'dataset_uscb.zip',
    'E0186': 'dataset_uscb.zip',
    # =========================================================================
    # Snyder-Tucker
    # =========================================================================
    'L0001': 'dataset_uscb.zip',
    # =========================================================================
    # Warren & Pearson
    # =========================================================================
    'L0002' or 'E0052': 'dataset_uscb.zip',
    'L0015': 'dataset_uscb.zip',
    'L0037': 'dataset_uscb.zip',
}

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

PPI = df['df_uscb'].add(1).cumprod()

plt.figure(1)
plt.plot(df)
plt.title('Chart$-$Price Index Comparison')
plt.xlabel('Period')
plt.ylabel('Price Index')
plt.grid()
plt.legend(['Revised Dataset', 'Cobb$-$Douglas Dataset'])
# =============================================================================
# plt.savefig('costIndexComparison.pdf', format='pdf', dpi=900)
# =============================================================================

plt.figure(2)
YEAR_BASE = 1958
plt.plot(PPI.rdiv(PPI[205]).mul(100), label=f'Price Index {YEAR_BASE}=100')
plt.title('Chart$-$Revised Price Index')
plt.xlabel('Period')
plt.ylabel('Price Index')
plt.legend()
plt.grid()
plt.show()

# =============================================================================
# TODO: Compare Above with BEA k* Series
# =============================================================================
# TODO: Current Price, Billions of Dollars:=P0119*PPI/PPI[205]

SERIES_IDS = {
    'E0183': 'dataset_uscb.zip',
    'E0184': 'dataset_uscb.zip',
    'E0185': 'dataset_uscb.zip',
}
stockpile_usa_hist(SERIES_IDS).pct_change().dropna(how='all').plot(grid=True)

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
# usa_cobb_douglas0010CostIndex.py
# =============================================================================


# =============================================================================
# Combine L1, L2 & P107/P110 for Period 1880--1932
# =============================================================================
# =============================================================================
# Results:
# {'E0183' or 'L0036': 'dataset_uscb.zip'}
# {'E0184' or 'L0038': 'dataset_uscb.zip'}
# {'E0185' or 'L0039': 'dataset_uscb.zip'}
# =============================================================================
SERIES_IDS = {
    'E0007': 'dataset_uscb.zip',
    'E0008': 'dataset_uscb.zip',
    'E0009': 'dataset_uscb.zip',
    'E0023': 'dataset_uscb.zip',
    'E0040': 'dataset_uscb.zip',
    'E0068': 'dataset_uscb.zip',
    'E0183': 'dataset_uscb.zip',
    'E0184': 'dataset_uscb.zip',
    'E0185': 'dataset_uscb.zip',
    'E0186': 'dataset_uscb.zip',
    # =========================================================================
    # Snyder-Tucker
    # =========================================================================
    'L0001': 'dataset_uscb.zip',
    # =========================================================================
    # Warren & Pearson
    # =========================================================================
    'L0002' or 'E0052': 'dataset_uscb.zip',
    'L0015': 'dataset_uscb.zip',
    'L0037': 'dataset_uscb.zip',
}

df = stockpile_usa_hist(SERIES_IDS | SERIES_IDS_PRCH).truncate(
    before=1885)

PPI = df.loc[:, 'P0107'].div(df.loc[:, 'P0110'])
PPI = 100*PPI/PPI[275]  # 1920
# =============================================================================
# TODO: Bootstrap PPI with pricesInverseXlSingle from project PricesConverter.py
# =============================================================================

plt.figure(1)
plt.plot(df.iloc[:, 1], label='L0001: Snyder-Tucker')
plt.plot(df.iloc[:, 2], label='L0002: Warren & Pearson')
plt.plot(df.iloc[:, 7], label='E0007')
plt.plot(df.iloc[:, 8], label='E0008')
plt.plot(df.iloc[:, 9], label='E0009')
plt.plot(df.iloc[:, 10], label='E0068')
plt.plot(df.iloc[235:, 0], PPI[235:],
         label=f'P107/P110, {df.iloc[275, 0]}=100')
plt.title('Price Index')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()
plt.figure(2)
plt.plot(df.iloc[:, 3])
plt.plot(df.iloc[:, 5])
plt.plot(df.iloc[:, 6])
plt.title('Price Index')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()
plt.show()

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

YEAR_BASE = 1958

df = stockpile_usa_hist(SERIES_IDS)

df['p110_over_p107'] = df.loc[:, 'P0110'].div(df.loc[:, 'P0107'])
df['p111_over_p108'] = df.loc[:, 'P0111'].div(df.loc[:, 'P0108'])
df['p112_over_p109'] = df.loc[:, 'P0112'].div(df.loc[:, 'P0109'])
df['x_index'] = df.loc[:, 'P0110'].div(
    df.loc[:, 'P0107']).div(df.loc[:, 'P0119'])
YEAR_BASE = 1958
df['x_index'] = df['x_index'].div(df.loc[YEAR_BASE, 'x_index'])
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
        f'$\\frac{{P110}}{{P107 \\times P119}}$, {YEAR_BASE}=100'
    ]
)
plt.title('Deflators')
plt.xlabel('Period')
plt.ylabel('Index')
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
    # Header: Y
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


YEAR_BASE = 1899
combine_cobb_douglas().pipe(
    transform_cobb_douglas, year_base=YEAR_BASE
)[0].pipe(transform_plot)

# =============================================================================
# usa_cobb_douglas0010Flow.py
# =============================================================================

SERIES_IDS = {
    'DT63AS02': 'dataset_douglas.zip',
    'J0149': 'dataset_uscb.zip',
    'J0150': 'dataset_uscb.zip',
    'J0151': 'dataset_uscb.zip',
    'P0107': 'dataset_uscb.zip',
    'P0108': 'dataset_uscb.zip',
    'P0109': 'dataset_uscb.zip',
}
YEAR_BASE = 1958

df = stockpile_usa_hist(SERIES_IDS_CD | SERIES_IDS)

SERIES_IDS = ['P0107', 'P0108', 'P0109']
df.loc[:, SERIES_IDS] = df.loc[:, SERIES_IDS].mul(1000)

LEGEND = ['CDT2S1', 'J0149', 'J0150', 'J0151']
plt.figure(1)
plt.plot(df.loc[:, LEGEND], label=LEGEND)
plt.title('Fixed Assets Increment')
plt.xlabel('Period')
plt.ylabel('Millions or Billions? Dollars')
plt.legend()
plt.grid()

LEGEND = ['P0107', 'P0108', 'P0109']
plt.figure(2)
plt.semilogy(df.loc[:, LEGEND], label=LEGEND)
plt.title('Fixed Assets Increment')
plt.xlabel('Period')
plt.ylabel('Millions or Billions? Dollars')
plt.legend()
plt.grid()

LEGEND = ['CDT2S3', 'DT63AS02']
plt.figure(3)
plt.plot(df.loc[:, LEGEND], label=LEGEND)
plt.title(f'Fixed Assets Increment, {YEAR_BASE}?=100')
plt.xlabel('Period')
plt.ylabel('Millions or Billions? Dollars')
plt.legend()
plt.grid()

LEGEND = ['CDT2S1', 'J0149', 'P0107']
plt.figure(4)
plt.semilogy(df.loc[:, LEGEND], label=LEGEND)
plt.title('Fixed Assets Increment, Cobb$-$Douglas, Census 1949 & 1975 Versions')
plt.xlabel('Period')
plt.ylabel('Millions or Billions? Dollars')
plt.legend()
plt.grid()
plt.show()
