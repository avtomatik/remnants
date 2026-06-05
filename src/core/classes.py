#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 19:22:22 2023

@author: green-machine
"""

import io
from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from typing import Any, Union

import pandas as pd
import requests

from core.paths import DATA_DIR


class Dataset(str, Enum):

    def __new__(cls, value: str, usecols: range):
        obj = str.__new__(cls)
        obj._value_ = value
        obj.usecols = usecols
        return obj

    DOUGLAS = "dataset_douglas.zip", range(4, 7)
    USA_COBB_DOUGLAS = "dataset_usa_cobb-douglas.zip", range(5, 8)
    USA_KENDRICK = "dataset_usa_kendrick.zip", range(4, 7)
    USA_MC_CONNELL = "dataset_usa_mc_connell_brue.zip", range(1, 4)
    USCB = "dataset_uscb.zip", range(9, 12)

    def get_kwargs(self) -> dict[str, Any]:

        NAMES = ["series_id", "period", "value"]

        return {
            "filepath_or_buffer": DATA_DIR / self.value,
            "header": 0,
            "names": NAMES,
            "index_col": 1,
            "usecols": self.usecols,
        }


class URL(Enum):
    FIAS = (
        "https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt"
    )
    NIPA = "https://apps.bea.gov/national/Release/TXT/NipaDataA.txt"

    def get_kwargs(self) -> dict[str, Any]:

        NAMES = ["series_ids", "period", "value"]

        kwargs = {
            "header": 0,
            "names": NAMES,
            "index_col": 1,
            "thousands": ",",
        }
        if requests.head(self.value).status_code == HTTPStatus.OK:
            kwargs["filepath_or_buffer"] = io.BytesIO(
                requests.get(self.value).content
            )
        else:
            kwargs["filepath_or_buffer"] = self.value.split("/")[-1]
        return kwargs


@dataclass(frozen=True, eq=True)
class SeriesID:
    series_id: str
    source: Union[Dataset, URL]


class Token(str, Enum):

    def __new__(
        cls,
        value: str,
        skiprows: Union[int, None],
        parse_dates: Union[bool, None],
    ):

        obj = str.__new__(cls)
        obj._value_ = value
        obj.skiprows = skiprows
        obj.parse_dates = parse_dates
        return obj

    USA_FRB = "dataset_usa_frb_invest_capital.csv", 4, None
    USA_FRB_G17 = "dataset_usa_frb_g17_all_annual_2013_06_23.csv", 1, None
    USA_FRB_US3 = "dataset_usa_frb_us3_ip_2018_09_02.csv", 7, True
    USA_NBER = "dataset_usa_nber_ces_mid_sic5811.csv", None, None

    def get_kwargs(self) -> dict[str, Any]:

        START = 5

        kwargs = {
            "filepath_or_buffer": DATA_DIR / self.value,
            "skiprows": self.skiprows,
            "parse_dates": self.parse_dates,
        }

        # =========================================================================
        # Load
        # =========================================================================
        df = pd.read_csv(**kwargs)

        MAP_NAMES = {
            "USA_FRB": map(int, df.columns[1:]),
            "USA_FRB_G17": map(int, map(float, df.columns[1 + START :])),
            "USA_FRB_US3": map(str.strip, df.columns[1:]),
            "USA_NBER": map(str.strip, df.columns[2:]),
        }

        return {
            "filepath_or_buffer": DATA_DIR / self.value,
            "skiprows": self.skiprows,
            "parse_dates": self.parse_dates,
            "header": 0,
            "index_col": 0,
            "names": ["period", *MAP_NAMES.get(self.name)],
            "usecols": (
                range(START, df.shape[1])
                if self.name == "USA_FRB_G17"
                else None
            ),
        }
