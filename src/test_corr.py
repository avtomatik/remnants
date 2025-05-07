import os

import pandas as pd
import seaborn as sns
from core.classes import Dataset
from core.config import DATA_DIR
from core.constants import SERIES_IDS, SERIES_IDS_PRCH
from core.funcs import stockpile, transform_deflator
from matplotlib import pyplot as plt


def get_data(series_ids: dict[str, str]) -> pd.DataFrame:
    return pd.concat(
        [
            stockpile(SERIES_IDS_PRCH).pipe(
                transform_deflator
            ).truncate(before=1885),
            stockpile(series_ids).pct_change(),
        ],
        axis=1
    )


def draw_heatmap(df: pd.DataFrame) -> None:
    """
    Draws Correlation Matrix, Pearson

    Parameters
    ----------
    df : pd.DataFrame
        DESCRIPTION.

    Returns
    -------
    None
        DESCRIPTION.

    """
    plt.figure(figsize=(12, 5))
    sns.heatmap(data=df.corr(), cmap="YlGnBu", annot=True)


def print_corr(df: pd.DataFrame, method: str) -> None:
    df_corr = df.corr(method=method)
    df_corr.loc['total_scores'] = df_corr.sum()
    print(
        f"Look At This: {df_corr.columns[df_corr.loc['total_scores'].argmin()]}"
    )
    print(df_corr)


def main():

    series_ids = enlist_series_ids(SERIES_IDS, Dataset.USCB)

    os.chdir(DATA_DIR)

    df = get_data(series_ids)

    df.pipe(draw_heatmap)

    for method in ['kendall', 'pearson', 'spearman']:
        df.pipe(print_corr, method)
    # Correlation Test Result: kendall & pearson & spearman: E0007, E0023, E0040, E0068, L0002, L0015


if __name__ == '__main__':
    main()
