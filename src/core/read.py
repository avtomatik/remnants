import datetime
import sqlite3
from typing import Any

import pandas as pd
from core.config import DATA_DIR


def read_usa_bea_pull_by_series_id(series_id: str) -> pd.DataFrame:
    """
    Retrieves Yearly Data for BEA Series' series_id
    Parameters
    ----------
    series_id : str
        DESCRIPTION.
    Returns
    -------
    pd.DataFrame
        DESCRIPTION.
    """
    DBNAME = "temporary"
    kwargs = {
        'filepath_or_buffer': 'dataset_usa_bea-nipa-2015-05-01.zip',
        'usecols': [0, *range(14, 18)],
    }
    _df = pd.read_csv(**kwargs)
    database = DATA_DIR.joinpath(f"{DBNAME}.db")
    with sqlite3.connect(database) as conn:
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
    _df = pd.DataFrame(
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


def read_usa_bea_sfat_pull_by_series_id(series_id: str) -> pd.DataFrame:
    """
    Retrieve Historical Manufacturing Series from BEA SFAT CSV File
    """

    NAMES = ['source_id', 'group1', 'series_id', 'period', 'value']
    USECOLS = [0, 6, 8, 9, 10]

    kwargs = {
        'filepath_or_buffer': 'dataset_usa_bea-nipa-2017-08-23-sfat.zip',
        'header': 0,
        'names': NAMES,
        'index_col': 3,
        'usecols': USECOLS,
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


def get_kwargs_gdelt(date: datetime.date) -> dict[str, Any]:
    """The GDELT Project"""

    return {
        'filepath_or_buffer': DATA_DIR.joinpath(f"dataset_world_{str(date).replace('-', '')}.export.csv"),
        'sep': '\t'
    }


def get_kwargs_usa_bls_cpiu() -> dict[str, Any]:
    """BLS CPI-U Price Index Fetch"""
    return {
        'filepath_or_buffer': 'dataset_usa_bls_cpiai.txt',
        'sep': '\s+',
        'index_col': 0,
        'usecols': range(13),
        'skiprows': 16,
    }
