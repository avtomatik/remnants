import sqlite3
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from thesis.src.lib.pull import pull_by_series_id
from thesis.src.lib.read import read_usa_bea_excel


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


# =============================================================================
# www.bea.gov/histdata/Releases/GDP_and_PI/2012/Q1/Second_May-31-2012/Section5ALL_Hist.xls
# =============================================================================
# =============================================================================
# Metadata: 'Section5ALL_Hist.xls'@['dataset_usa_bea-release-2010-08-05 Section5ALL_Hist.xls' Offsets 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip']"""
# =============================================================================
def read_pull_K160021():
    kwargs = {
        'archive_name': 'dataset_usa_bea-release-2013-01-31-SectionAll_xls_1929_1969.zip',
        'wb_name': 'Section5ALL_Hist.xls',
        'sh_name': '50900 Ann',
    }
    # =============================================================================
    # Fixed Assets Series: K160021, 1951--1969
    # =============================================================================
    SERIES_ID = 'K160021'
    return read_usa_bea_excel(**kwargs).loc[:, [SERIES_ID]]


def read_pull_for_autocorrelation(filepath_or_buffer: str, series_id: str) -> DataFrame:
    """
    Parameters
    ----------
    filepath_or_buffer : str
        'datasetAutocorrelation.txt' | 'CHN_TUR_GDP.zip'.
    series_id : str
        DESCRIPTION.
    Returns
    -------
    DataFrame
        DESCRIPTION.
    """
    kwargs = {
        'filepath_or_buffer': filepath_or_buffer,
        'names': ('period', 'series_id', 'value'),
        'index_col': 0,
        'skiprows': 1
    }
    return pd.read_csv(**kwargs).pipe(pull_by_series_id, series_id)