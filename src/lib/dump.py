#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 16:24:57 2022

@author: Alexander Mikhailov
"""


# =============================================================================
# Stores Unused or Test Codes
# =============================================================================
import os
import sqlite3
from pathlib import Path

import pandas as pd
from lib.collect import stockpile_usa_bea
from lib.read import read_temporary, read_usa_bea_excel
from pandas import DataFrame

from remnants.src.constants import SERIES_IDS_LAB
from thesis.src.lib.test import (test_subtract_a, test_subtract_b,
                                 test_usa_bea_sfat_series_ids,
                                 test_usa_bea_subtract)

# =============================================================================
# Separate Chunk of Code
# =============================================================================


# =============================================================================
# Separate Block
# =============================================================================
def test_data_capital_combined_archived():
    """Data Test"""
    kwargs = {
        # =====================================================================
        # ONE ARCHIVE NAME
        # =====================================================================
        'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'wb_name': 'Section1ALL_Hist.xls',
        # =====================================================================
        # ONE SHEET NAME
        # =====================================================================
        'sh_name': '10105 Ann'
    }
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1
        # =====================================================================
        'A191RC1',
    )
    df_control = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )
    # =========================================================================
    # OTHER SHEET NAME
    # =========================================================================
    kwargs['sh_name'] = '10505 Ann'
    df_test = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )

    if df_control.equals(df_test):
        print("Series 'A006RC1' & 'A191RC1' @ Worksheet '10105 Ann' Equals Series 'A006RC1' & 'A191RC1' @ Worksheet '10505 Ann' for Period 1929--1969")
    else:
        print("Data Varies from Worksheet '10105 Ann' to Worksheet '10505 Ann'")

    kwargs = {
        # =====================================================================
        # OTHER ARCHIVE NAME
        # =====================================================================
        'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
        'wb_name': 'Section1all_xls.xls',
        # =====================================================================
        # ONE SHEET NAME
        # =====================================================================
        'sh_name': '10105 Ann'
    }
    df_control = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )
    # =========================================================================
    # OTHER SHEET NAME
    # =========================================================================
    kwargs['sh_name'] = '10505 Ann'
    df_test = pd.concat(
        map(lambda _: read_usa_bea_excel(**kwargs).loc[:, _], SERIES_IDS),
        axis=1
    )

    if df_control.equals(df_test):
        print("Series 'A006RC1' & 'A191RC1' @ Worksheet '10105 Ann' Equals Series 'A006RC1' & 'A191RC1' @ Worksheet '10505 Ann' for Period 1969--2012")
    else:
        print("Data Varies from Worksheet '10105 Ann' to Worksheet '10505 Ann'")


def test_data_capital_combined_archived():
    """Data Test"""
    # =========================================================================
    # Nominal Investment Series: A006RC1, 1929--1969
    # =========================================================================
    ARCHIVE_NAMES = (
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1969_2012.zip',
    )
    WB_NAMES = (
        'Section1ALL_Hist.xls',
        'Section1all_xls.xls',
    )
    SH_NAME_CONTROL, SH_NAME_TEST = '10105 Ann', '10505 Ann'
    SERIES_IDS = (
        # =====================================================================
        # Nominal Investment Series: A006RC1
        # =====================================================================
        'A006RC1',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC1
        # =====================================================================
        'A191RC1'
    )
    df_control = pd.concat(
        [
            read_usa_bea_excel(
                archive_name, wb_name, SH_NAME_CONTROL
            ).loc[:, SERIES_IDS]
            for archive_name, wb_name in zip(ARCHIVE_NAMES, WB_NAMES)
        ]
    ).drop_duplicates()
    df_test = pd.concat(
        [
            read_usa_bea_excel(
                archive_name, wb_name, SH_NAME_TEST
            ).loc[:, SERIES_IDS]
            for archive_name, wb_name in zip(ARCHIVE_NAMES, WB_NAMES)
        ]
    ).drop_duplicates()
    if df_control.equals(df_test):
        print(
            """
            Series "A006RC1" & "A191RC1" @ Worksheet "10105 Ann" Equals Series "A006RC1" & "A191RC1" @ Worksheet "10505 Ann"
            """
        )
    else:
        print(
            """
            Data Varies from Worksheet "10105 Ann" to Worksheet "10505 Ann"
            """
        )


def collect_usa_bls_cpiu() -> DataFrame:
    """BLS CPI-U Price Index Fetch"""
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_bls_cpiai.txt',
        'sep': '\s+',
        'index_col': 0,
        'usecols': range(13),
        'skiprows': 16,
    }
    df = pd.read_csv(**kwargs)
    df.rename_axis('period', inplace=True)
    df['mean'] = df.mean(axis=1)
    df['sqrt'] = df.iloc[:, :-1].prod(1).pow(1/12)
    # =========================================================================
    # Tests
    # =========================================================================
    df['mean_less_sqrt'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    df['dec_on_dec'] = df.iloc[:, -3].pct_change()
    df['mean_on_mean'] = df.iloc[:, -4].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)


def read_usa_bea_pull_by_series_id(series_id: str) -> DataFrame:
    """
    Retrieves Yearly Data for BEA Series' series_id
    Parameters
    ----------
    series_id : str
        DESCRIPTION.
    Returns
    -------
    DataFrame
        DESCRIPTION.
    """
    DIR = "/home/green-machine/data_science"
    DBNAME = "temporary"
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_bea-nipa-2015-05-01.zip',
        'usecols': [0, *range(14, 18)],
    }
    _df = pd.read_csv(**kwargs)
    with sqlite3.connect(Path(DIR).joinpath(f"{DBNAME}.db")) as conn:
        cursor = conn.cursor()
        _df.to_sql("temporary", conn, if_exists="replace", index=False)
        stmt = f"""
        SELECT * FROM temporary
        WHERE
            series_id = '{series_id}'
            AND subperiod = 0
            ;
        """
        cursor = conn.execute(stmt)
    _df = DataFrame(
        cursor.fetchall(),
        columns=['source_id', 'series_id', 'period', 'sub_period', 'value'],
    )
    _df.set_index('period', inplace=True)
    _df.drop('sub_period', axis=1, inplace=True)
    df = pd.concat(
        [
            _df[_df.iloc[:, 0] == source_id].iloc[:, [2]].drop_duplicates()
            for source_id in sorted(set(_df.iloc[:, 0]))
        ],
        axis=1
    )
    df.columns = [
        ''.join((source_id.split()[1].replace('.', '_'), series_id))
        for source_id in sorted(set(_df.iloc[:, 0]))
    ]
    return df


def read_usa_bea_pull_by_series_id(df: DataFrame, series_id: str) -> DataFrame:
    """
    Retrieve Yearly Data for BEA Series ID
    """
    df = df[df.loc[:, "series_id"] == series_id]
    source_ids = sorted(set(df.loc[:, "source_id"]))
    chunk = pd.concat(
        [
            df[df.loc[:, "source_id"] == source_id].iloc[:, [-1]].drop_duplicates()
            for source_id in source_ids
        ],
        axis=1,
        sort=True
    )
    chunk.columns = [
        ''.join((source_id.split()[1].replace('.', '_'), series_id))
        for source_id in source_ids
    ]
    return chunk


def collect_usa_xlsm() -> DataFrame:
    FILE_NAME = 'dataset_usa_0025_p_r.txt'
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC, 1929--2021
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Nominal Gross Domestic Product Series: A191RC, 1929--2021
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX, 1929--2021
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal National income Series: A032RC, 1929--2021
        # =====================================================================
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
    }
    return pd.concat(
        [
            stockpile_usa_bea(SERIES_IDS),
            read_temporary(FILE_NAME),
        ],
        axis=1
    )


def collect_usa_bea_labor() -> DataFrame:
    """
    Labor Series: A4601C0, 1929--2013
    """
    SERIES_IDS = {
        'A4601C': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt'
    }
    return stockpile_usa_bea(SERIES_IDS)


DIR = '/media/green-machine/KINGSTON'

os.chdir(DIR)

# =============================================================================
# www.bea.gov/histdata/Releases/GDP_and_PI/2012/Q1/Second_May-31-2012/Section5ALL_Hist.xls
# =============================================================================
# =============================================================================
# Metadata: 'Section5ALL_Hist.xls'@['dataset_usa_bea-release-2010-08-05 Section5ALL_Hist.xls' Offsets 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip']"""
# =============================================================================
kwargs = {
    'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
    'wb_name': 'Section5ALL_Hist.xls',
    'sh_name': '50900 Ann',
}
# =============================================================================
# Fixed Assets Series: K160021, 1951--1969
# =============================================================================
SERIES_ID = 'K160021'
df = read_usa_bea_excel(**kwargs).loc[:, (SERIES_ID, )]

# =============================================================================
# Not Clear
# =============================================================================
kwargs = {
    'filepath_or_buffer': 'dataset_read_can-{:08n}-eng-{}.csv'.format(
        310003, 7591839622055840674
    ),
    'skiprows': 3,
}
df = pd.read_csv(**kwargs)


KWARGS = (
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1929--1969
    # =========================================================================
    {
        'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1929_1969.zip',
        'wb_name': 'Section1ALL_Hist.xls',
        'sh_name': '10105 Ann',
    },
    # =========================================================================
    # Nominal Gross Domestic Product Series: A191RC1, 1969--2014
    # =========================================================================
    {
        'archive_name': 'dataset_usa_bea-release-2015-02-27-SectionAll_xls_1969_2015.zip',
        'wb_name': 'Section1all_xls.xls',
        'sh_name': '10105 Ann',
    },
)
SERIES_ID = 'A191RC1'
df_semi_d = pd.concat(
    [read_usa_bea_excel(**kwargs).loc[:, (SERIES_ID,)] for kwargs in KWARGS],
    sort=True
).drop_duplicates()
# =============================================================================
# Gross fixed capital formation Data Block
# =============================================================================
# =============================================================================
# Not Clear:
{
    "table": 3800068,
    "title": "Gross fixed capital formation",
    "geo": "Canada",
    "prices": "Chained (2007) dollars",
    "seas": "Seasonally adjusted at annual rates",
    "estimates": "Industrial machinery and equipment (x 1,000,000)",
    "frequency_start_end": "(quarterly, 1961-03-01 to 2017-09-01)",
    "series_id": "v62143969"
}
# =============================================================================
# =============================================================================
# Not Clear:
{
    "table": 3800068,
    "title": "Gross fixed capital formation",
    "geo": "Canada",
    "prices": "Chained (2007) dollars",
    "seas": "Seasonally adjusted at annual rates",
    "estimates": "Industrial machinery and equipment (x 1,000,000)",
    "frequency_start_end": "(quarterly, 1961-03-01 to 2017-09-01)",
    "series_id": "v62143990"
}


def read_usa_bea_sfat_pull_by_series_id(series_id: str) -> DataFrame:
    """
    Retrieve Historical Manufacturing Series from BEA SFAT CSV File
    """
    MAP = {
        'source_id': 0, 'group1': 6, 'series_id': 8, 'period': 9, 'value': 10
    }
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_bea-nipa-2017-08-23-sfat.zip',
        'header': 0,
        'names': tuple(MAP.keys()),
        'index_col': 3,
        'usecols': tuple(MAP.values()),
    }
    df = pd.read_csv(**kwargs)

    _filter = (
        (df.loc[:, "source_id"].str.contains('Historical')) &
        (df.loc[:, "group1"].str.contains('Manufacturing')) &
        (df.loc[:, "series_id"] == series_id)
    )
    df.drop(["group1", "series_id"], axis=1, inplace=True)

    source_ids = sorted(set(df.loc[:, "source_id"]))

    chunk = pd.concat(
        [
            df[df.loc[:, "source_id"] == source_id].iloc[:, [-1]].drop_duplicates()
            for source_id in source_ids
        ],
        axis=1,
        sort=True
    )
    chunk.columns = [
        ''.join((source_id.split()[1].replace('.', '_'), series_id))
        for source_id in source_ids
    ]
    return chunk


def plot_usa_un_former() -> None:
    """
    https://unstats.un.org/unsd/snaama/Index

    Returns
    -------
    None
        DESCRIPTION.

    """
    kwargs = {
        "io": "dataset_world_united-nations-Download-GDPcurrent-USD-countries.xls",
        "index_col": 0,
        "skiprows": 2,
    }
    _df = pd.read_excel(**kwargs)
    _df = _df[_df.iloc[:, 0] == 'Gross Domestic Product (GDP)']
    _df = _df.select_dtypes(exclude=['object']).transpose()
    df = pd.DataFrame()
    df['us_to_world'] = _df.loc[:, 'United States'].div(_df.sum(axis=1))
    df.plot(grid=True)


def combine_usa_general() -> DataFrame:
    """
    Returns
    -------
    DataFrame
        DESCRIPTION.
    """
    FILE_NAME = "dataset_usa_0025_p_r.txt"
    SERIES_ID = {'X0414': 'dataset_uscb.zip'}
    SERIES_IDS = {
        # =====================================================================
        # Nominal Investment Series: A006RC
        # =====================================================================
        'A006RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Implicit Price Deflator Series: A006RD
        # =====================================================================
        'A006RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross private domestic investment -- Nonresidential: A008RC
        # =====================================================================
        'A008RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Implicit Price Deflator -- Gross private domestic investment -- Nonresidential: A008RD
        # =====================================================================
        'A008RD': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal National income Series: A032RC
        # =====================================================================
        'A032RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross Domestic Product, 2012=100: A191RA
        # =====================================================================
        'A191RA': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Nominal Gross Domestic Product Series: A191RC
        # =====================================================================
        'A191RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Real Gross Domestic Product Series, 2012=100: A191RX
        # =====================================================================
        'A191RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross Domestic Investment, W170RC
        # =====================================================================
        'W170RC': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Gross Domestic Investment, W170RX
        # =====================================================================
        'W170RX': 'https://apps.bea.gov/national/Release/TXT/NipaDataA.txt',
        # =====================================================================
        # Fixed Assets Series: k1n31gd1es00
        # =====================================================================
        'k1n31gd1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Investment in Fixed Assets and Consumer Durable Goods, Private
        # =====================================================================
        'i3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Chain-Type Quantity Indexes for Investment in Fixed Assets and Consumer Durable Goods, Private
        # =====================================================================
        'icptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
        # =====================================================================
        # Historical-Cost Net Stock of Private Fixed Assets, Private Fixed Assets, k3ptotl1es00
        # =====================================================================
        'k3ptotl1es00': 'https://apps.bea.gov/national/FixedAssets/Release/TXT/FixedAssets.txt',
    }
    return pd.concat(
        [
            pd.concat(
                [
                    pd.concat(
                        [
                            read_usa_bea(SERIES_IDS[series_id]).pipe(
                                pull_by_series_id, series_id)
                            for series_id in tuple(SERIES_IDS)[:8]
                        ],
                        axis=1
                    ),
                    stockpile_usa_bea(SERIES_IDS_LAB).pipe(
                        transform_mean, name="bea_labor_mfg"),
                    pd.concat(
                        [
                            read_usa_bea(SERIES_IDS[series_id]).pipe(
                                pull_by_series_id, series_id)
                            for series_id in tuple(SERIES_IDS)[8:]
                        ],
                        axis=1
                    ),
                ],
                axis=1,
                sort=True
            ),
            read_usa_frb_h6(),
            stockpile_usa_hist(SERIES_ID),
            read_temporary(FILE_NAME),
        ],
        axis=1
    )


def test_data_consistency_d():
    """Project IV: USA Macroeconomic & Fixed Assets Data Tests"""
    # =========================================================================
    # Macroeconomic Data Tests
    # =========================================================================
    def _generate_kwargs_list(
            archive_name: str,
            wb_name: str,
            sheet_names: tuple[str],
            series_ids: tuple[str]
    ) -> list[dict]:
        return [
            {
                'archive_name': archive_name,
                'wb_name': wb_name,
                'sh_name': _sh,
                'series_id': series_id,
            } for _sh, series_id in zip(sheet_names, series_ids)
        ]

    # =========================================================================
    # Tested: "A051RC" != "A052RC" + "A262RC"
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10705-A', 'T11200-A', 'T10705-A')
    SERIES_IDS = ('A051RC', 'A052RC', 'A262RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Tested: "Government" = "Federal" + "State and local"
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A')
    SERIES_IDS = ('A822RC', 'A823RC', 'A829RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30100-A', 'T30200-A', 'T30300-A')
    SERIES_IDS = ('A955RC', 'A957RC', 'A991RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Tested: "Federal" = "National defense" + "Nondefense"
    # =========================================================================
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section1all_xls.xlsx'
    SH_NAMES = ('T10105-A', 'T10105-A', 'T10105-A')
    SERIES_IDS = ('A823RC', 'A824RC', 'A825RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    ARCHIVE_NAME = 'dataset_usa_bea-release-2019-12-19-Survey.zip'
    WB_NAME = 'Section3all_xls.xlsx'
    SH_NAMES = ('T30200-A', 'T30905-A', 'T30905-A')
    SERIES_IDS = ('A957RC', 'A997RC', 'A542RC')
    test_usa_bea_subtract(
        _generate_kwargs_list(ARCHIVE_NAME, WB_NAME, SH_NAMES, SERIES_IDS)
    )
    # =========================================================================
    # Fixed Assets Data Tests
    # =========================================================================
    df = test_usa_bea_sfat_series_ids()

    test_subtract_a()
    # =========================================================================
    # Comparison of "k3n31gd1es00" out of df_control with "k3n31gd1es00" out of df_test
    # =========================================================================
    test_subtract_b(df)
    # =========================================================================
    # Future Project: Test Ratio of Manufacturing Fixed Assets to Overall Fixed Assets
    # =========================================================================
    # =========================================================================
    # TODO:
    # =========================================================================
    return


def filter_data_frame(df: DataFrame, query: dict[str]) -> DataFrame:
    for column, criterion in query['filter'].items():
        df = df[df.iloc[:, column] == criterion]
    return df
