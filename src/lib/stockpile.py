import pandas as pd
from pandas import DataFrame

from remnants.src.lib.read import read_usa_bea_excel


def stockpile_usa_bea_excel_zip(kwargs_list: list[dict], series_ids: list[str]) -> DataFrame:
    """
    Parameters
    ----------
    kwargs_list : list[dict]
        DESCRIPTION.
    series_ids : list[str]
        DESCRIPTION.
    Returns
    -------
    DataFrame
        DESCRIPTION.
    """
    return pd.concat(
        map(
            lambda _: read_usa_bea_excel(**_[0]).loc[:, [_[-1]]],
            zip(kwargs_list, series_ids)
        ),
        axis=1,
        sort=True
    )