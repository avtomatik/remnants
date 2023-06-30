import os

import pandas as pd
import seaborn as sns
from core.constants import SERIES_IDS, SERIES_IDS_PRCH
from core.funcs import stockpile_usa_hist, transform_deflator
from matplotlib import pyplot as plt
from pandas import DataFrame


def get_data(series_ids: dict[str, str]) -> DataFrame:
    return pd.concat(
        [
            stockpile_usa_hist(SERIES_IDS_PRCH).pipe(
                transform_deflator
            ).truncate(before=1885),
            stockpile_usa_hist(series_ids).pct_change(),
        ],
        axis=1
    )


def draw_heatmap(df: DataFrame) -> None:
    """
    Draws Correlation Matrix, Pearson

    Parameters
    ----------
    df : DataFrame
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    plt.figure(figsize=(12, 5))
    sns.heatmap(data=df.corr(), cmap="YlGnBu", annot=True)


def print_corr(df: DataFrame, method: str) -> None:
    df_corr = df.corr(method=method)
    df_corr.loc['total_scores'] = df_corr.sum()
    print(
        f"Look At This: {df_corr.columns[df_corr.loc['total_scores'].argmin()]}"
    )
    print(df_corr)


def main():
    PATH = '/media/green-machine/KINGSTON'
    ARCHIVE_NAME = 'dataset_uscb.zip'

    series_ids = dict.fromkeys(SERIES_IDS, ARCHIVE_NAME)

    os.chdir(PATH)

    df = get_data(series_ids)

    df.pipe(draw_heatmap)

    for method in ['kendall', 'pearson', 'spearman']:
        df.pipe(print_corr, method)
    # Correlation Test Result: kendall & pearson & spearman: E0007, E0023, E0040, E0068, L0002, L0015


if __name__ == '__main__':
    main()
