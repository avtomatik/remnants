'''Project: Capital Retirement'''
# =============================================================================
# capital_retirement.yaml
# =============================================================================
from itertools import product

import pandas as pd
from lib.tools import collect_capital_combined_archived
from pandas import DataFrame

from remnants.src.plot_capital_retirement import plot_capital_retirement


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
    SERIES_IDS_LAB = {
        # =====================================================================
        # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
        # =====================================================================
        # =====================================================================
        # 1929--1948
        # =====================================================================
        'H4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # 1948--1987
        # =====================================================================
        'J4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # 1987--2000
        # =====================================================================
        'A4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # 1998--2020
        # =====================================================================
        'N4313C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
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


def main(df):
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
    YM = _df.iloc[:, 3].mul(100).div(_df.iloc[:, 4])
    # =========================================================================
    # Capital, End-Period, Not Adjusted
    # =========================================================================
    C = _df.iloc[:, 6].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    L = _df.iloc[:, 7]
    plot_capital_retirement(I, Y, YN, C, L)
    plot_capital_retirement(I, YM, YN, C, L)


STARTS = {22: 1951, 38: 1967}
STOPS = {83: 2011}
BOUNDS = tuple(product(STARTS, STOPS))

df = collect_capital_combined_archived()

if __name__ == '__main__':
    main(df, 38, 83)
