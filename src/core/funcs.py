#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 20:44:03 2023

@author: green-machine
"""


import io
from functools import cache
from pathlib import Path

import pandas as pd
import requests
from core.constants import MAP_READ_USA_HIST
from pandas import DataFrame


@cache
def read_usa_bea(url: str) -> DataFrame:
    """
    Retrieves U.S. Bureau of Economic Analysis DataFrame from URL

    Parameters
    ----------
    url : str

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    """
    kwargs = {
        'header': 0,
        'names': ('series_ids', 'period', 'value'),
        'index_col': 1,
        'thousands': ','
    }
    if requests.head(url).status_code == 200:
        kwargs['filepath_or_buffer'] = io.BytesIO(requests.get(url).content)
    else:
        kwargs['filepath_or_buffer'] = url.split('/')[-1]
    return pd.read_csv(**kwargs)


@cache
def read_usa_frb() -> DataFrame:
    """


    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    """
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_frb_invest_capital.csv',
        'skiprows': 4,
    }
    # =========================================================================
    # Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = ('period', *map(int, df.columns[1:]))
    kwargs['index_col'] = 0
    # =========================================================================
    # Re-Load
    # =========================================================================
    return pd.read_csv(**kwargs).transpose()


@cache
def read_usa_hist(filepath_or_buffer: str) -> DataFrame:
    """
    Retrieves Data from Enumerated Historical Datasets
    Parameters
    ----------
    filepath_or_buffer : str

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    """
    kwargs = {
        'filepath_or_buffer': filepath_or_buffer,
        'header': 0,
        'names': tuple(MAP_READ_USA_HIST.get(filepath_or_buffer).keys()),
        'index_col': 1,
        'skiprows': (0, 4)[filepath_or_buffer == 'dataset_usa_brown.zip'],
        'usecols': tuple(MAP_READ_USA_HIST.get(filepath_or_buffer).values()),
    }
    return pd.read_csv(**kwargs)


def pull_by_series_id(df: DataFrame, series_id: str) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    series_id : str

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================
    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id].iloc[:, [1]].rename(
        columns={"value": series_id}
    )


def stockpile_usa_bea(series_ids: dict[str, str]) -> DataFrame:
    """


    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================

    """
    return pd.concat(
        map(
            lambda _: read_usa_bea(_[-1]).pipe(pull_by_series_id, _[0]),
            series_ids.items()
        ),
        axis=1,
        sort=True
    )


def stockpile_usa_hist(series_ids: dict[str, str]) -> DataFrame:
    """


    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================

    """
    return pd.concat(
        map(
            lambda _: read_usa_hist(_[-1]).pipe(pull_by_series_id, _[0]),
            series_ids.items()
        ),
        axis=1,
        sort=True
    )


def transform_usa_frb_fa_def(df: DataFrame) -> DataFrame:
    """
    Retrieves DataFrame for Deflator for Manufacturing Fixed Assets Series

    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator
        ================== =================================

    """
    df['fa_def_frb'] = (df.iloc[:, [1, 4]].sum(axis=1)).div(
        df.iloc[:, [0, 3]].sum(axis=1))
    return df.iloc[:, [-1]]


def transform_deflator(df: DataFrame) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal
        df.iloc[:, 1]      Real
        ================== =================================

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator PRC
        ================== =================================
    """
    assert df.shape[1] == 2
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['prc'] = df.iloc[:, -1].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)


def transform_mean(df: DataFrame, name: str) -> DataFrame:
    """


    Parameters
    ----------
    df : DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    name : str
        New Column Name.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Sum of <series_ids>
        ================== =================================
    """
    df[name] = df.mean(axis=1)
    return df.iloc[:, [-1]]


def construct_usa_hist_deflator(series_ids: dict[str, str]) -> DataFrame:
    """
    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.
    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator PRC
        ================== =================================
    """
    return stockpile_usa_hist(series_ids).pipe(transform_deflator)


def read_temporary(
    file_name: str, path_src: str = '/home/green-machine/data_science/data/interim'
) -> DataFrame:
    """


    Parameters
    ----------
    file_name : str
        DESCRIPTION.
    path_src : str, optional
        DESCRIPTION. The default is '/home/green-machine/data_science/data/interim'.

    Returns
    -------
    DataFrame
        DESCRIPTION.

    """
    kwargs = {
        'filepath_or_buffer': Path(path_src).joinpath(file_name),
        'index_col': 0,
    }
    return pd.read_csv(**kwargs)