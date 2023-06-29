#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 10:21:08 2023

@author: green-machine
"""


import re

import pandas as pd
from pandas import DataFrame


def lash_up_ewm(df: DataFrame, window: int = 5, alpha: float = 0.5) -> DataFrame:
    """
    Single Exponential Smoothing
    Robert Goodell Brown, 1956

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Target Series
        ================== =================================.
    window : int, optional
        DESCRIPTION. The default is 5.
    alpha : float, optional
        DESCRIPTION. The default is 0.5.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    ses = [
        lash_up_ewm_core(
            df.iloc[0, -1],
            # =================================================================
            # Average of Window-First Entries
            # =================================================================
            df.iloc[:window, -1].mean(),
            alpha
        )
    ]

    for _ in range(1, df.shape[0]):
        ses.append(lash_up_ewm_core(df.iloc[_, -1], ses[-1], alpha))

    df[f'ses{window:02d}_{alpha:,.6f}'] = ses
    return df


def lash_up_ewm_core(current: float, cumulated: float, alpha: float) -> float:
    return alpha * current + (1 - alpha) * cumulated


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
    _df = df.reset_index(level=0).copy()
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
