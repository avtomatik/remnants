#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 27 20:44:03 2023

@author: green-machine
"""


import io
import zipfile
from functools import cache
from typing import Any, Union

import numpy as np
import pandas as pd
import requests
import scipy.optimize as optimization
from core.classes import URL, Dataset, SeriesID
from core.config import DATA_DIR


def enlist_series_ids(series_ids: list[str], source: Union[Dataset, URL]) -> list[SeriesID]:
    return list(map(lambda _: SeriesID(_, source), series_ids))


@cache
def read_source(series_id: SeriesID) -> pd.DataFrame:
    """


    Parameters
    ----------
    series_id : SeriesID
        DESCRIPTION.

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================.

    """
    return pd.read_csv(**series_id.source.get_kwargs())


def stockpile(series_ids: list[SeriesID]) -> pd.DataFrame:
    """


    Parameters
    ----------
    series_ids : list[SeriesID]
        DESCRIPTION.

    Returns
    -------
    pd.DataFrame
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


def pull_by_series_id(df: pd.DataFrame, series_id: SeriesID) -> pd.DataFrame:
    """


    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series IDs
        df.iloc[:, 1]      Values
        ================== =================================.
    series_id : SeriesID
        DESCRIPTION.

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Series
        ================== =================================.

    """
    assert df.shape[1] == 2
    return df[df.iloc[:, 0] == series_id.series_id].iloc[:, [1]].rename(
        columns={'value': series_id.series_id}
    )


def transform_deflator(df: pd.DataFrame) -> pd.DataFrame:
    """


    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Nominal
        df.iloc[:, 1]      Real
        ================== =================================

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator PRC
        ================== =================================
    """
    assert df.shape[1] == 2
    df['deflator'] = df.iloc[:, 0].div(df.iloc[:, 1])
    df['prc'] = df.iloc[:, -1].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)


def transform_mean(df: pd.DataFrame, name: str) -> pd.DataFrame:
    """


    Parameters
    ----------
    df : pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    name : str
        New Column Name.

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Sum of <series_ids>
        ================== =================================
    """
    df[name] = df.mean(axis=1)
    return df.iloc[:, [-1]]


def construct_usa_hist_deflator(series_ids: dict[str, str]) -> pd.DataFrame:
    """
    Parameters
    ----------
    series_ids : dict[str, str]
        DESCRIPTION.
    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Deflator PRC
        ================== =================================
    """
    return stockpile(series_ids).pipe(transform_deflator)


def read_worldbank(
    source_id: str,
    url_template: str = 'https://api.worldbank.org/v2/en/indicator/{}?downloadformat=csv'
) -> pd.DataFrame:
    """
    Returns pd.DataFrame with World Bank API
    Parameters
    ----------
    source_id : str
        Like ('NY.GDP.MKTP.CD').
    url_template : str, optional
        DESCRIPTION. The default is 'https://api.worldbank.org/v2/en/indicator/{}?downloadformat=csv'.
    Returns
    -------
    pd.DataFrame
    """
    kwargs = {
        'index_col': 0,
        'skiprows': 4
    }
    with zipfile.ZipFile(io.BytesIO(requests.get(url_template.format(source_id)).content)) as archive:
        # =====================================================================
        # Select the Largest File with min() Function
        # =====================================================================
        with archive.open(
            min({_.filename: _.file_size for _ in archive.filelist})
        ) as f:
            kwargs['filepath_or_buffer'] = f
            df = pd.read_csv(**kwargs).dropna(axis=1, how='all').transpose()
            return df.drop(df.index[:3]).rename_axis('period')


def calculate_curve_fit_params(df: pd.DataFrame) -> None:
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
    return {
        'filepath_or_buffer': DATA_DIR.joinpath(file_name),
        'index_col': 0,
    }
