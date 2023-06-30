import pandas as pd
from core.constants import SERIES_IDS_LAB
from pandas import DataFrame

from thesis.src.lib.combine import combine_usa_money
from thesis.src.lib.pull import pull_by_series_id
from thesis.src.lib.read import (read_temporary, read_usa_bea,
                                 read_usa_frb_g17, read_usa_fred)
from thesis.src.lib.stockpile import stockpile_usa_bea
from thesis.src.lib.transform import transform_mean


def combine_usa_xlsm() -> DataFrame:
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC, 1929--2021
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal National income Series: A032RC, 1929--2021
        # =====================================================================
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    }
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            read_temporary(FILE_NAME),
        ],
        axis=1
    )


def combine_usa_general() -> DataFrame:
    """
    Returns
    -------
    DataFrame
        DESCRIPTION.
    """
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Implicit Price Deflator Series: A006RD
        # =====================================================================
        'A006RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross private domestic investment -- Nonresidential: A008RC
        # =====================================================================
        'A008RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD
        # =====================================================================
        'A008RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal National income Series: A032RC
        # =====================================================================
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross Domestic Product, 2012=100: A191RA
        # =====================================================================
        'A191RA': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross Domestic Investment, W170RC
        # =====================================================================
        'W170RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross Domestic Investment, W170RX
        # =====================================================================
        'W170RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Investment in Fixed Assets and Consumer Durable Goods, Private
        # =====================================================================
        'i3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Chain-Type Quantity Indexes for Investment in Fixed Assets and Consumer Durable Goods, Private
        # =====================================================================
        'icptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es00
        # =====================================================================
        'k3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    return pd.concat(
        [
            pd.concat(
                [
                    pd.concat(
                        [
                            read_usa_bea(SERIES_IDS[series_id]).pipe(
                                pull_by_series_id, series_id)
                            for series_id in tuple(SERIES_IDS)[:8]
                        ],
                        axis=1
                    ),
                    stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                        transform_mean, name='bea_labor_mfg'
                    ),
                    pd.concat(
                        [
                            read_usa_bea(SERIES_IDS[series_id]).pipe(
                                pull_by_series_id, series_id)
                            for series_id in tuple(SERIES_IDS)[8:]
                        ],
                        axis=1
                    ),
                ],
                axis=1,
                sort=True
            ),
            combine_usa_money(),
            read_temporary(FILE_NAME),
        ],
        axis=1
    )


def combine_usa_bea_gdp() -> DataFrame:
    """
    USA BEA Gross Domestic Product
    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal
        df.iloc[:, 1]      Real
        ================== =================================
    """
    SERIES_IDS = {
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    }
    return stockpile_usa_bea(SERIES_IDS)


def transform_def(df: DataFrame) -> DataFrame:
    """
    Cumulative Price Index

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal
        df.iloc[:, 1]      Real
        ================== =================================.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Product Deflator
        ================== =================================.

    """
    df['deflator_gdp'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    return df.iloc[:, [-1]]


def combine_bea_def_from_file() -> DataFrame:
    """
    Returns Cumulative Price Index for Some Base Year from Certain Type BEA Deflator File
    -------
    DataFrame
        DESCRIPTION.
    """
    kwargs = {
        "io": "../../data/external/dataset_usa_bea-GDPDEF.xls",
        "names": ('period', 'deflator_gdp'),
        "index_col": 0,
        "skiprows": 15,
        "parse_dates": True
    }
    df = pd.read_excel(**kwargs)
    return df.groupby(df.index.year).prod().pow(1/4)


def combine_usa_investment_capital() -> DataFrame:
    SERIES_ID = 'PPIACO'
    SERIES_IDS = {
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    } | {
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    } or {
        # =====================================================================
        # Fixed Assets Series: K10070
        # =====================================================================
        'K10070': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    } or {
        # =========================================================
        # U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis;
        # https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
        # http://www.bea.gov/data/economic-accounts/national
        # https://fred.stlouisfed.org/series/K160491A027NBEA
        # https://search.bea.gov/search?affiliate=u.s.bureauofeconomicanalysis&query=k160491
        # =========================================================
        # =========================================================
        # 'K16049' Replaced with 'K10070' in 'combine_combined_archived()'
        # =========================================================
        'K16049': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    return pd.concat(
        [
            # =================================================================
            # Producer Price Index
            # =================================================================
            read_usa_fred(SERIES_ID),
            stockpile_usa_bea(SERIES_IDS)
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)


def combine_usa_macroeconomics() -> DataFrame:
    """Data Fetch"""
    SERIES_ID = 'CAPUTL.B50001.A'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX, 1929--2021, 2012=100
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Deflator Gross Domestic Product, A191RD, 1929--2021, 2012=100
        # =====================================================================
        'A191RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # National Income: A032RC, 1929--2021
        # =====================================================================
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: K10070, 1951--2021
        # =====================================================================
        'K10070' or 'K10002': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: k1ntotl1si00, 1925--2020
        # =====================================================================
        'k1ntotl1si00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Fixed Assets Series: k3ntotl1si00, 1925--2020
        # =====================================================================
        'k3ntotl1si00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1925--2020
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Fixed Assets Series: k3n31gd1es00, 1925--2020
        # =====================================================================
        'k3n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, [SERIES_ID]].dropna(axis=0),
        ],
        axis=1,
        sort=True
    )


def combine_capital_combined_archived() -> DataFrame:
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX1, 1929--2012
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: K160021, 1951--2011
        # =====================================================================
        # =====================================================================
        # K10002 << K100021 << K160021
        # =====================================================================
    } | {
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    } or {
        # =====================================================================
        # Fixed Assets Series: K10070
        # =====================================================================
        'K10070' or 'K16002': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    } or {
        # =========================================================
        # U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis;
        # https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
        # http://www.bea.gov/data/economic-accounts/national
        # https://fred.stlouisfed.org/series/K160491A027NBEA
        # https://search.bea.gov/search?affiliate=u.s.bureauofeconomicanalysis&query=k160491
        # =========================================================
        # =========================================================
        # 'K16049' Replaced with 'K10070' in 'combine_combined_archived()'
        # =========================================================
        'K16049': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, ['CAPUTL.B50001.A']].dropna(axis=0),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Labor Series: A4601C
            # =================================================================
            stockpile_usa_bea(
                {'A4601C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'}
            )
        ],
        axis=1,
        sort=True
    )


def combine_usa_investment_turnover_bls() -> DataFrame:
    SERIES_ID = 'PPIACO'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    } | {
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    } or {
        # =====================================================================
        # Fixed Assets Series: K10070
        # =====================================================================
        'K10070': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    } or {
        # =========================================================
        # U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis;
        # https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
        # http://www.bea.gov/data/economic-accounts/national
        # https://fred.stlouisfed.org/series/K160491A027NBEA
        # https://search.bea.gov/search?affiliate=u.s.bureauofeconomicanalysis&query=k160491
        # =========================================================
        # =========================================================
        # 'K16049' Replaced with 'K10070' in 'combine_combined_archived()'
        # =========================================================
        'K16049': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    df = pd.concat(
        [
            # =================================================================
            # Producer Price Index
            # =================================================================
            read_usa_fred(SERIES_ID),
            stockpile_usa_bea(SERIES_IDS),
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)
    # =========================================================================
    # Deflator, 2012=100
    # =========================================================================
    df['deflator'] = df.iloc[:, 0].add(1).cumprod()
    df.iloc[:, -1] = df.iloc[:, -1].rdiv(df.loc[2012, df.columns[-1]])
    # =========================================================================
    # Investment, 2012=100
    # =========================================================================
    df['investment'] = df.iloc[:, 1].mul(df.iloc[:, -1])
    # =========================================================================
    # Capital, 2012=100
    # =========================================================================
    df['capital'] = df.iloc[:, 3].mul(df.iloc[:, -1])
    # =========================================================================
    # Capital Retirement Ratio
    # =========================================================================
    df['ratio_mu'] = df.iloc[:, -2].mul(1).sub(df.iloc[:, -1].shift(-1)).div(
        df.iloc[:, -1]).add(1)
    return (
        df.loc[:, ['investment', 'A191RX',
                   'capital', 'ratio_mu']].dropna(axis=0),
        df.loc[:, ['ratio_mu']].dropna(axis=0),
    )


def combine_combined_archived() -> DataFrame:
    """Version: 02 December 2013"""

    SERIES_IDS = {
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A006RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A008RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A008RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RA': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'W170RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'W170RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    }
    # =========================================================================
    # US BEA Fixed Assets Series Tests
    # =========================================================================

    SERIES_IDS_SFAT = ({
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    } or {
        # =====================================================================
        # Fixed Assets Series: K10070
        # =====================================================================
        'K10070': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    } or {
        # =========================================================
        # U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis;
        # https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
        # http://www.bea.gov/data/economic-accounts/national
        # https://fred.stlouisfed.org/series/K160491A027NBEA
        # https://search.bea.gov/search?affiliate=u.s.bureauofeconomicanalysis&query=k160491
        # =========================================================
        # =========================================================
        # 'K16049' Replaced with 'K10070' in 'combine_combined_archived()'
        # =========================================================
        'K16049': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }) | {
        # =====================================================================
        # Investment in Fixed Assets, Private, i3ptotl1es00, 1901--2016
        # =====================================================================
        'i3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Chain-Type Quantity Index for Investment in Fixed Assets, Private, icptotl1es00, 1901--2016
        # =====================================================================
        'icptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Current-Cost Net Stock of Fixed Assets, Private, k1ptotl1es00, 1925--2016
        # =====================================================================
        'k1ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es00, 1925--2016
        # =====================================================================
        'k3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Chain-Type Quantity Indexes for Net Stock of Fixed Assets, Private, kcptotl1es00, 1925--2016
        # =====================================================================
        'kcptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            stockpile_usa_bea(SERIES_IDS_SFAT),
            combine_usa_money(),
            pd.read_csv(FILE_NAME, index_col=0),
        ],
        axis=1,
        sort=True
    )


def combine_local() -> DataFrame:

    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC1, 1929--2012
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC1, 1929--2012
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2005=100: A191RX1, 1929--2012
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    } | {
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt'
    } or {
        # =====================================================================
        # Fixed Assets Series: K10070
        # =====================================================================
        'K10070': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    } or {
        # =========================================================
        # U.S. Bureau of Economic Analysis, Produced assets, closing balance: Fixed assets (DISCONTINUED) [K160491A027NBEA], retrieved from FRED, Federal Reserve Bank of St. Louis;
        # https://fred.stlouisfed.org/series/K160491A027NBEA, August 23, 2018.
        # http://www.bea.gov/data/economic-accounts/national
        # https://fred.stlouisfed.org/series/K160491A027NBEA
        # https://search.bea.gov/search?affiliate=u.s.bureauofeconomicanalysis&query=k160491
        # =========================================================
        # =========================================================
        # 'K16049' Replaced with 'K10070' in 'combine_combined_archived()'
        # =========================================================
        'K16049': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            # =================================================================
            # U.S. Bureau of Economic Analysis (BEA), Manufacturing Labor Series
            # =================================================================
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name='bea_labor_mfg'
            ),
            read_usa_frb_g17().loc[:, ['CAPUTL.B50001.A']].dropna(axis=0),
        ],
        axis=1,
        sort=True
    )
