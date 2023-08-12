#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:03:14 2023

@author: green-machine
"""


import matplotlib.pyplot as plt
import pandas as pd
from core.classes import Dataset
from core.constants import (SERIES_IDS_CB, SERIES_IDS_CD, SERIES_IDS_COL,
                            SERIES_IDS_PRCH)
from core.funcs import construct_usa_hist_deflator, stockpile, transform_mean

# =============================================================================
# uscb_cost_index.py
# =============================================================================

YEAR_BASE = 1958
# =============================================================================
# Combine E0007, E0023, E0040, E0068, L0002, L0015 & P107/P110
# =============================================================================
# =============================================================================
# TODO: Bureau of Labor Statistics: PPIACO
# =============================================================================

df = pd.concat(
    [
        pd.concat(
            [
                stockpile(SERIES_IDS_CB).pct_change(),
                construct_usa_hist_deflator(SERIES_IDS_PRCH)
            ],
            axis=1
        ).dropna(how='all').pipe(transform_mean, name='df_uscb'),
        construct_usa_hist_deflator(SERIES_IDS_CD)
    ],
    axis=1,
    sort=True
)

LABEL = ['Revised Dataset', 'Cobb$-$Douglas Dataset']
plt.figure(1)
plt.plot(df, label=LABEL)
plt.title('Chart$-$Price Index Comparison')
plt.xlabel('Period')
plt.ylabel('Price Index')
plt.grid()
plt.legend()
# =============================================================================
# plt.savefig('uscb_cost_index_comparison.pdf', format='pdf', dpi=900)
# =============================================================================

df['price_index'] = df['df_uscb'].add(1).cumprod()

plt.figure(2)

plt.plot(
    df.loc[:, 'price_index'].div(df.loc[YEAR_BASE, 'price_index']).mul(100),
    label=f'Price Index {YEAR_BASE}=100'
)
plt.title('Chart$-$Revised Price Index')
plt.xlabel('Period')
plt.ylabel('Price Index')
plt.legend()
plt.grid()
plt.show()

# =============================================================================
# TODO: DONE: Compared with 'kcn31gd1es00': False
# =============================================================================


# =============================================================================
# usa_cobb_douglas0010_cost_index.py
# =============================================================================
# =============================================================================
# Combine E0007, E0023, E0040, E0068, L0002, L0015 & P107/P110
# =============================================================================
# =============================================================================
# TODO: Bureau of Labor Statistics: PPIACO
# =============================================================================

df = stockpile(SERIES_IDS_CB).pct_change()

SERIES_IDS = [
    'E0007',
    'E0023',
    'E0040',
    'E0068',
    # =========================================================================
    # Warren & Pearson
    # =========================================================================
    'L0002' or 'E0052',
    'L0015',
]

plt.figure(1)
plt.plot(df.loc[:, SERIES_IDS], label=SERIES_IDS)
plt.plot(
    construct_usa_hist_deflator(SERIES_IDS_PRCH).truncate(before=1885),
    label='price_index'
)
plt.title('Price Index')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()


plt.figure(2)
plt.plot(
    stockpile(
        enlist_series_ids(SERIES_IDS_COL, Dataset.USCB)
    ).pct_change(),
    label=SERIES_IDS_COL
)
plt.title('Cost-of-Living Indexes')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()
plt.show()

# =============================================================================
# usa_cobb_douglas0002.py
# =============================================================================
# =============================================================================
# Census Manufacturing Fixed Assets Series
# =============================================================================


# =============================================================================
# TODO: Re-Confirm Below Series
# =============================================================================

SERIES_IDS = dict.fromkeys(
    map(lambda _: f'P{_:04}', range(107, 123)), Dataset.USCB
)

df = stockpile(SERIES_IDS)

df['p110_over_p107'] = df.loc[:, 'P0110'].div(df.loc[:, 'P0107'])
df['p111_over_p108'] = df.loc[:, 'P0111'].div(df.loc[:, 'P0108'])
df['p112_over_p109'] = df.loc[:, 'P0112'].div(df.loc[:, 'P0109'])

plt.figure(1)
plt.semilogy(df.iloc[:, :-3])
plt.title('Purchases of Structures and Equipment')
plt.xlabel('Period')
plt.ylabel('Billions, USD')
plt.grid()
plt.legend()

LABEL = [
    '$\\frac{P110}{P107}$',
    '$\\frac{P111}{P108}$',
    '$\\frac{P112}{P109}$',
]

plt.figure(2)
plt.plot(df.iloc[:, -3:].pct_change().truncate(before=1885), label=LABEL)
plt.title('Deflators')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()
plt.show()


# =============================================================================
# usa_cobb_douglas0010_flow.py
# =============================================================================

SERIES_IDS = {
    'DT63AS01': Dataset.DOUGLAS,
    'J0149': Dataset.USCB,
    'J0150': Dataset.USCB,
    'J0151': Dataset.USCB,
    'P0107': Dataset.USCB,
    'P0108': Dataset.USCB,
    'P0109': Dataset.USCB,
}


df = stockpile(SERIES_IDS_CD | SERIES_IDS)


LABEL = ['CDT2S1', 'J0149', 'J0150', 'J0151']
plt.figure(1)
plt.plot(df.loc[:, LABEL].pct_change(), label=LABEL)
plt.title('Nominal Fixed Assets Increment Rate')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()

LABEL = ['P0107', 'P0108', 'P0109']
plt.figure(2)
plt.plot(df.loc[:, LABEL].pct_change().truncate(before=1885), label=LABEL)
plt.title('Nominal Fixed Assets Increment Rate')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()

LABEL = ['CDT2S3', 'DT63AS01']
plt.figure(3)
plt.plot(df.loc[:, LABEL].pct_change(), label=LABEL)
plt.title('Real Fixed Assets Increment Rate')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()

LABEL = ['CDT2S1', 'J0149', 'P0107']
plt.figure(4)
plt.plot(df.loc[:, LABEL].pct_change(), label=LABEL)
plt.title('Fixed Assets Increment, Cobb$-$Douglas, Census 1949 & 1975 Versions')
plt.xlabel('Period')
plt.ylabel('Index')
plt.legend()
plt.grid()
plt.show()
