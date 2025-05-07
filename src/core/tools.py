#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 10:21:08 2023

@author: green-machine
"""


import pandas as pd


def lash_up_ewm(df: pd.DataFrame, window: int = 5, alpha: float = 0.5) -> pd.DataFrame:
    """
    Single Exponential Smoothing
    Robert Goodell Brown, 1956

    Parameters
    ----------
    df : pd.DataFrame
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
    pd.DataFrame
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


def transform_center_by_period(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Target Series
        ================== =================================
    Returns
    -------
    pd.DataFrame
    """
    # =========================================================================
    # TODO: Any Use?
    # =========================================================================
    # =========================================================================
    # pd.DataFrame for Results
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
