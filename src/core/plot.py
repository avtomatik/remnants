from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame


def plot_usa_un_former() -> None:
    """
    https://unstats.un.org/unsd/snaama/Index
    Returns
    -------
    None
        DESCRIPTION.
    """

    _df = pd.read_excel(**get_kwargs_usa_un())
    _df = _df[_df.iloc[:, 0] == 'Gross Domestic Product (GDP)']
    _df = _df.select_dtypes(exclude=['object']).transpose()
    df = DataFrame()
    df['us_to_world'] = _df.loc[:, 'United States'].div(_df.sum(axis=1))
    df.plot(grid=True)


def get_kwargs_usa_un() -> dict[str, Any]:
    return {
        "io": "dataset_world_united-nations-Download-GDPcurrent-USD-countries.xls",
        "index_col": 0,
        "skiprows": 2,
    }


def plot_turnover_take_one(df: DataFrame) -> None:
    """
        ================== =================================
        df.index           Period
        df.iloc[:, 0]      Capital
        df.iloc[:, 1]      Product
        ================== =================================
    """
    df['c_turnover'] = df.iloc[:, 1].div(df.iloc[:, 0])
    plt.figure(1)
    plt.plot(df.iloc[:, 2], df.iloc[:, 0])
    plt.title(
        'Fixed Assets Volume to Fixed Assets Turnover, {}$-${}'.format(
            *df.index[[0, -1]]
        )
    )
    plt.xlabel('Fixed Assets Turnover')
    plt.ylabel('Fixed Assets Volume')
    plt.grid()
    plt.figure(2)
    plt.plot(df.iloc[:, 2], label='Fixed Assets Turnover')
    plt.title('Fixed Assets Turnover, {}$-${}'.format(*df.index[[0, -1]]))
    plt.xlabel('Period')
    plt.ylabel('Fixed Assets Turnover')
    plt.grid()
    plt.legend()
    plt.show()
