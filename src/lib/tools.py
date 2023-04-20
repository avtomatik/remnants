#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 10:21:08 2023

@author: green-machine
"""


import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame

from constants import SERIES_IDS_LAB
from thesis.src.lib.collect import stockpile_usa_bea
from thesis.src.lib.pull import pull_by_series_id
from thesis.src.lib.read import read_usa_frb_g17
from thesis.src.lib.transform import transform_mean


def collect_usa_bea_def() -> DataFrame:
    """
    USA BEA Gross Domestic Product Deflator: Cumulative Price Index

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Gross Domestic Product Deflator
        ================== =================================

    """
    df = collect_usa_bea_gdp()
    df['deflator_gdp'] = df.iloc[:, 0].div(df.iloc[:, 1]).mul(100)
    return df.iloc[:, [-1]]


def collect_usa_bea_gdp() -> DataFrame:
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


def collect_bea_def_from_file() -> DataFrame:
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


def collect_capital_combined_archived() -> DataFrame:
    SERIES_ID = 'CAPUTL.B50001.A'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC, 1929--2021
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series: A191RX, 1929--2021
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00, 1925--2020
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            # =================================================================
            # Capacity Utilization Series: CAPUTL.B50001.A, 1967--2012
            # =================================================================
            read_usa_frb_g17().loc[:, (SERIES_ID,)].dropna(axis=0),
            # =================================================================
            # Manufacturing Labor Series: _4313C0, 1929--2020
            # =================================================================
            stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                transform_mean, name="bea_labor_mfg"),
            # =================================================================
            # For Overall Labor Series, See: A4601C0, 1929--2020
            # =================================================================
            collect_usa_bea_labor()
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)


def collect_usa_investment_capital() -> DataFrame:
    SERIES_IDS = {
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: K10070
        # =====================================================================
        'K10070': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    return pd.concat(
        [
            collect_usa_bls_cpiu(),
            stockpile_usa_bea(SERIES_IDS)
        ],
        axis=1,
        sort=True
    ).dropna(axis=0)


def lash_up_ewm(df: DataFrame, window: int = 5, alpha: float = 0.5) -> DataFrame:
    """
    Single Exponential Smoothing
    Robert Goodell Brown, 1956
        ================== =================================
        df.iloc[:, 0]      Period
        df.iloc[:, 1]      Target Series
        ================== =================================
    """
    # =========================================================================
    # Average of Window-First Entries
    # =========================================================================
    _mean = df.iloc[:window, 1].mean()

    ses = []
    ses.append(alpha * df.iloc[0, 1] + (1 - alpha) * _mean)
    for _ in range(1, df.shape[0]):
        ses.append(alpha * df.iloc[_, 1] + (1 - alpha) * ses[_ - 1])

    ses = DataFrame(ses, columns=[f'ses{window:02d}_{alpha:,.6f}'])
    _df = pd.concat([df, ses], axis=1, sort=True)
    _df = _df.set_index('period')
    return _df


def plot_filter_kol_zur(period, series) -> None:
    '''Kolmogorov--Zurbenko Filter'''
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Results
    # =========================================================================
    filter_kol_zur = DataFrame()
    filter_kol_zur = pd.concat([filter_kol_zur, period], axis=1)
    filter_kol_zur = pd.concat([filter_kol_zur, series], axis=1)
    # =========================================================================
    # DataFrame for Kolmogorov--Zurbenko Filter Residuals
    # =========================================================================
    df_rkzf = DataFrame()
    df_rkzf = pd.concat([df_rkzf, period], axis=1)
    df_rkzf = pd.concat([df_rkzf, period.rolling(window=2).mean()], axis=1)
    df_rkzf = pd.concat([df_rkzf, (series.diff())/series.shift(1)], axis=1)
    for k in range(1, 1+period.shape[0]) // 2:
        cap = 'col'+str(k).zfill(2)
        skz = DataFrame(np.nan, index=range(period.shape[0]), columns=[cap])
        for j in range(1, 1+len(period)-k):
            vkz = 0
            for i in range(1+k):
                vkz += series[i+j-1]*np.special.binom(k, i)/(2**k)
            skz[cap][i+j-k // 2-1] = vkz
        filter_kol_zur = pd.concat([filter_kol_zur, skz], axis=1)
        if k % 2 == 0:
            df_rkzf = pd.concat([df_rkzf, (skz.diff())/skz.shift(1)], axis=1)
        else:
            df_rkzf = pd.concat([df_rkzf, skz.pct_change(1).shift(-1)], axis=1)
    plt.figure(1)
    plt.title('Kolmogorov$-$Zurbenko Filter')
    plt.xlabel('Period')
    plt.ylabel('Measure')
    plt.scatter(
        filter_kol_zur.iloc[:, 0], filter_kol_zur.iloc[:, 1], label='Original Series')
    for i in range(2, 1+len(period) // 2):
        if i % 2 == 0:
            plt.plot(filter_kol_zur.iloc[:, 0].rolling(window=2).mean(),
                     filter_kol_zur.iloc[:, i], label='$filter_kol_zur(\\lambda=%d)$' % (i-1))
        else:
            plt.plot(filter_kol_zur.iloc[:, 0], filter_kol_zur.iloc[:, i],
                     label='$filter_kol_zur(\\lambda=%d)$' % (i-1))
    plt.grid()
    plt.legend()
    plt.figure(2)
    plt.title('Kolmogorov$-$Zurbenko Filter Residuals')
    plt.xlabel('Period')
    plt.ylabel('Unity')
    plt.scatter(df_rkzf.iloc[:, 1], df_rkzf.iloc[:, 2], label='Residuals')
    for i in range(3, 2+len(period) // 2):
        if i % 2 == 0:
            plt.plot(df_rkzf.iloc[:, 1], df_rkzf.iloc[:, i],
                     label='$\\delta filter_kol_zur(\\lambda=%d)$' % (i-1))
        else:
            plt.plot(df_rkzf.iloc[:, 0], df_rkzf.iloc[:, i],
                     label='$\\delta filter_kol_zur(\\lambda=%d)$' % (i-1))
    plt.grid()
    plt.legend()
    plt.show()


def pull_can_capital(df: DataFrame) -> list[str]:
    """
    Retrieves Series IDs from Statistics Canada -- Fixed Assets Tables
    """
    {
        "table": "031-0004",
        "title": "Flows and stocks of fixed non-residential capital, total all industries, by asset, provinces and territories, annual (dollars x 1,000,000)",
        "file_name": "dataset_can_00310004-eng.zip"
    }
    _filter = (
        (df.iloc[:, 2].str.contains('2007 constant prices')) &
        (df.iloc[:, 4] == 'Geometric (infinite) end-year net stock') &
        (df.iloc[:, 5].str.contains('Industrial', flags=re.IGNORECASE))
    )
    {
        "table": "36-10-0238-01 (formerly CANSIM 031-0004)",
        "title": "Flows and stocks of fixed non-residential capital, total all industries, by asset, provinces and territories, annual (dollars x 1,000,000)"
    }
    _filter = (
        (df.iloc[:, 3].str.contains('2007 constant prices')) &
        (df.iloc[:, 5] == 'Straight-line end-year net stock') &
        (df.iloc[:, 6].str.contains('Industrial', flags=re.IGNORECASE))
    )
    return sorted(set(df[_filter].loc[:, "VECTOR"]))


def read_pull_for_autocorrelation(filepath_or_buffer: str, series_id: str) -> DataFrame:
    """


    Parameters
    ----------
    filepath_or_buffer : str
        'datasetAutocorrelation.txt' | 'CHN_TUR_GDP.zip'.
    series_id : str
        DESCRIPTION.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    kwargs = {
        'filepath_or_buffer': filepath_or_buffer,
        'names': ('period', 'series_id', 'value'),
        'index_col': 0,
        'skiprows': 1
    }
    return pd.read_csv(**kwargs).pipe(pull_by_series_id, series_id)


def strip_deflator(df: DataFrame, col_num: int) -> DataFrame:
    return df.iloc[:, (col_num,)].dropna(axis=0).pct_change().dropna(axis=0)


def transform_center_by_period(df: DataFrame) -> DataFrame:
    """
    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    Returns
    -------
    DataFrame
    """
    # =========================================================================
    # TODO: Any Use?
    # =========================================================================
    # =========================================================================
    # DataFrame for Results
    # =========================================================================
    _df = df.copy()
    _df.reset_index(level=0, inplace=True)
    period = _df.iloc[:, 0]
    series = _df.iloc[:, 1]
    # =========================================================================
    # Loop
    # =========================================================================
    for _ in range(_df.shape[0] // 2):
        period = period.rolling(2).mean()
        series = series.rolling(2).mean()
        period_roll = period.shift(-((1 + _) // 2))
        series_roll = series.shift(-((1 + _) // 2))
        _df = pd.concat(
            [
                _df,
                period_roll,
                series_roll,
                series_roll.div(_df.iloc[:, 1]),
                series_roll.shift(-2).sub(series_roll).div(
                    series_roll.shift(-1)).div(2),
            ],
            axis=1,
            sort=True
        )
    return _df
