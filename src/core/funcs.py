#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 20:44:03 2023

@author: green-machine
"""


import io
from functools import cache
from pathlib import Path
from typing import Any
from zipfile import ZipFile

import numpy as np
import pandas as pd
import requests
import scipy.optimize as optimization
from core.classes import SeriesID
from pandas import DataFrame


@cache
def read_source(series_id: SeriesID) -> DataFrame:
    """


    Parameters
    ----------
    series_id : SeriesID
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================.

    """
    return pd.read_csv(**series_id.source.get_kwargs())


def stockpile(series_ids: list[SeriesID]) -> DataFrame:
    """


    Parameters
    ----------
    series_ids : list[SeriesID]
        DESCRIPTION.

    Returns
    -------
    DataFrame
        ================== =================================
        df.index           Period
        ...                ...
        df.iloc[:, -1]     Values
        ================== =================================.

    """
    return pd.concat(
        map(
            lambda _: read_source(_).pipe(pull_by_series_id, _),
            series_ids
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
    return stockpile(series_ids).pipe(transform_deflator)


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


def get_pre_kwargs(file_name: str) -> dict[str, Any]:
    """
    Returns `kwargs` for `pd.read_csv()` for Usual Cases

    Parameters
    ----------
    file_name : str
        DESCRIPTION.

    Returns
    -------
    dict[str, Any]
        DESCRIPTION.

    """
    PATH_SRC = '/home/green-machine/data_science/data/interim'
    return {
        'filepath_or_buffer': Path(PATH_SRC).joinpath(file_name),
        'index_col': 0,
    }
