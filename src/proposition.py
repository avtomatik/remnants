#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 22:01:25 2023

@author: green-machine
"""


import pandas as pd

from core.classes import Token
from core.paths import DATA_DIR


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
    FILE_NAME = "dataset_usa_frb_g17_all_annual_2013_06_23.csv"
    kwargs = {
        "filepath_or_buffer": DATA_DIR / FILE_NAME,
        "skiprows": 1,
    }
    # =========================================================================
    # Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    kwargs["header"] = 0
    kwargs["names"] = (
        "period",
        *map(int, map(float, df.columns[1 + _start :])),
    )
    kwargs["index_col"] = 0
    kwargs["usecols"] = range(_start, df.shape[1])
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
    FILE_NAME = "dataset_usa_frb_us3_ip_2018_09_02.csv"
    kwargs = {
        "filepath_or_buffer": DATA_DIR / FILE_NAME,
        "skiprows": 7,
        "parse_dates": True,
    }
    # =========================================================================
    # Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    kwargs["header"] = 0
    kwargs["names"] = ("period", *map(str.strip, df.columns[1:]))
    kwargs["index_col"] = 0
    # =========================================================================
    # Re-Load
    # =========================================================================
    df = pd.read_csv(**kwargs)
    return df.groupby(df.index.year).mean()


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
