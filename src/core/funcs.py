#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 20:44:03 2023

@author: green-machine
"""


import io
from functools import cache
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd
import requests
import scipy.optimize as optimization
from core.classes import Token
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
def read_usa_hist(token: Token) -> DataFrame:
    """
    Retrieves Data from Enumerated Historical Datasets
    Parameters
    ----------
    token : Token

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================
    """

    return pd.read_csv(**token.get_kwargs())


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


def read_worldbank(
    source_id: str,
    url_template: str = 'https://api.worldbank.org/v2/en/indicator/{}?downloadformat=csv'
) -> DataFrame:
    """
    Returns DataFrame with World Bank API
    Parameters
    ----------
    source_id : str
        Like ('NY.GDP.MKTP.CD').
    url_template : str, optional
        DESCRIPTION. The default is 'https://api.worldbank.org/v2/en/indicator/{}?downloadformat=csv'.
    Returns
    -------
    DataFrame
    """
    kwargs = {
        'index_col': 0,
        'skiprows': 4
    }
    with ZipFile(io.BytesIO(requests.get(url_template.format(source_id)).content)) as archive:
        # =====================================================================
        # Select the Largest File with min() Function
        # =====================================================================
        with archive.open(
            min({_.filename: _.file_size for _ in archive.filelist})
        ) as f:
            kwargs['filepath_or_buffer'] = f
            df = pd.read_csv(**kwargs).dropna(axis=1, how='all').transpose()
            return df.drop(df.index[:3]).rename_axis('period')


def calculate_curve_fit_params(df: DataFrame) -> None:
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Labor Capital Intensity
        df.iloc[:, 1]      Labor Productivity
        ================== =================================
    """

    def _curve(regressor: pd.Series, b: float, k: float) -> pd.Series:
        return regressor.pow(k).mul(b)

    params, _matrix = optimization.curve_fit(
        _curve,
        df.iloc[:, -2],
        df.iloc[:, -1],
        np.array([1.0, 0.5])
    )
    print('Factor, b: {:,.4f}; Index, k: {:,.4f}'.format(*params))
