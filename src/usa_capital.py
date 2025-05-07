#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 12:59:39 2023

@author: green-machine
"""


import matplotlib.pyplot as plt
import pandas as pd
from thesis.src.lib.combine import combine_usa_capital

# =============================================================================
# usa_capital.py
# =============================================================================
# =============================================================================
# TODO: Make More Robust Adjustment
# =============================================================================


def transform_cobb_douglas_extension_capital(df: pd.DataFrame) -> pd.DataFrame:
    """Manufacturing Fixed Assets Series Comparison"""
    # =========================================================================
    # TODO: Adjust Multiples of 1000
    # =========================================================================
    SERIES_IDS = ['P0107', 'P0110', 'P0119', 'frb_nominal', 'frb_real']
    df.loc[:, SERIES_IDS] = df.loc[:, SERIES_IDS].mul(1000)

    # =========================================================================
    # Nominal Fixed Assets Values, Billions of Dollars, as per Cobb--Douglas: Revised
    # =========================================================================
    df['nominal_cbb_dg'] = df.loc[:, 'CDT2S1'].mul(
        df.loc[:, 'CDT2S4']).div(df.loc[:, 'CDT2S3'])
    df['nominal_uscb'] = df.loc[:, 'P0107'].mul(
        df.loc[:, 'P0119']).div(df.loc[:, 'P0110'])
    return df


df = combine_usa_capital().truncate(before=1869).pipe(
    transform_cobb_douglas_extension_capital
)

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
