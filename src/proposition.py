#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 22:01:25 2023

@author: green-machine
"""


from enum import Enum
from functools import cache
from typing import Any, Union

import pandas as pd
from core.config import DATA_DIR


class Token(str, Enum):

    def __new__(cls, value: str, skiprows: Union[int, None], parse_dates: Union[bool, None]):

        obj = str.__new__(cls)
        obj._value_ = value
        obj.skiprows = skiprows
        obj.parse_dates = parse_dates
        return obj

    USA_FRB = 'dataset_usa_frb_invest_capital.csv', 4, None
    USA_FRB_G17 = 'dataset_usa_frb_g17_all_annual_2013_06_23.csv', 1, None
    USA_FRB_US3 = 'dataset_usa_frb_us3_ip_2018_09_02.csv', 7, True
    USA_NBER = 'dataset_usa_nber_ces_mid_sic5811.csv', None, None

    def get_kwargs(self) -> dict[str, Any]:

        START = 5

        kwargs = {
            'filepath_or_buffer': DATA_DIR.joinpath(self.value),
            'skiprows': self.skiprows,
            'parse_dates': self.parse_dates
        }

        # =========================================================================
        # Load
        # =========================================================================
        df = pd.read_csv(**kwargs)

        MAP_NAMES = {
            'USA_FRB': map(int, df.columns[1:]),
            'USA_FRB_G17': map(int, map(float, df.columns[1 + START:])),
            'USA_FRB_US3': map(str.strip, df.columns[1:]),
            'USA_NBER': map(str.strip, df.columns[2:]),
        }

        return {
            'filepath_or_buffer': DATA_DIR.joinpath(self.value),
            'skiprows': self.skiprows,
            'parse_dates': self.parse_dates,
            'header': 0,
            'index_col': 0,
            'names': ['period', *MAP_NAMES.get(self.name)],
            'usecols': range(
                START, df.shape[1]
            ) if self.name == 'USA_FRB_G17' else None
        }


@cache
def read_usa_frb() -> pd.DataFrame:
    """


    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    """
    FILE_NAME = 'dataset_usa_frb_invest_capital.csv'
    kwargs = {
        'filepath_or_buffer': DATA_DIR.joinpath(FILE_NAME),
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


def read_usa_frb_g17() -> pd.DataFrame:
    """


    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    """
    _start = 5
    FILE_NAME = 'dataset_usa_frb_g17_all_annual_2013_06_23.csv'
    kwargs = {
        'filepath_or_buffer': DATA_DIR.joinpath(FILE_NAME),
        'skiprows': 1,
    }
    # =========================================================================
    # Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = (
        'period', *map(int, map(float, df.columns[1 + _start:]))
    )
    kwargs['index_col'] = 0
    kwargs['usecols'] = range(_start, df.shape[1])
    # =========================================================================
    # Re-Load
    # =========================================================================
    return pd.read_csv(**kwargs).transpose()


def read_usa_frb_us3() -> pd.DataFrame:
    """


    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    """
    # =========================================================================
    # TODO: https://www.federalreserve.gov/datadownload/Output.aspx?rel=g17&filetype=zip
    # =========================================================================
    # =========================================================================
    # with zipfile.ZipFile('FRB_g17.zip').open('G17_data.xml') as f:
    # =========================================================================
    FILE_NAME = 'dataset_usa_frb_us3_ip_2018_09_02.csv'
    kwargs = {
        'filepath_or_buffer': DATA_DIR.joinpath(FILE_NAME),
        'skiprows': 7,
        'parse_dates': True
    }
    # =========================================================================
    # Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = ('period', *map(str.strip, df.columns[1:]))
    kwargs['index_col'] = 0
    # =========================================================================
    # Re-Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    return df.groupby(df.index.year).mean()


def read_usa_nber(filepath_or_buffer: str) -> pd.DataFrame:
    """


    Parameters
    ----------
    filepath_or_buffer : str
        DESCRIPTION.
    agg : str
        ("mean" | "sum").

    Returns
    -------
    pd.DataFrame
        ================== =================================
        df.index           Period
        df.iloc[:, ...]    Series
        ================== =================================
    """
    kwargs = {'filepath_or_buffer': filepath_or_buffer}
    # =========================================================================
    # Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    kwargs['header'] = 0
    kwargs['names'] = ('period', *map(str.strip, df.columns[2:]))
    kwargs['index_col'] = 0
    # =========================================================================
    # Re-Load
    # =========================================================================
    return pd.read_csv(**kwargs)


# =============================================================================
# for token in list(Token):
#     print(pd.read_csv(**token.get_kwargs()))
# =============================================================================


df = pd.read_csv(**Token.USA_FRB.get_kwargs()).transpose()
print(df)

df = pd.read_csv(**Token.USA_FRB_G17.get_kwargs()).transpose()
print(df)

df = pd.read_csv(**Token.USA_FRB_US3.get_kwargs())
print(df.groupby(df.index.year).mean())

df = pd.read_csv(**Token.USA_NBER.get_kwargs())
print(df)
