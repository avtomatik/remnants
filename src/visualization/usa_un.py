# -*- coding: utf-8 -*-
"""
Created on Sat May  2 22:26:24 2020

@author: Alexander Mikhailov
"""


import pandas as pd
from core.read import get_kwargs_unstats
from pandas import DataFrame


def main() -> None:
    """
    Visualizes the U.S. Contribution to World`s Gross Domestic Product (GDP)

    Parameters
    ----------
    url : str, optional

    Returns
    -------
    None.

    """
    _df = pd.read_excel(**get_kwargs_unstats())
    _df = _df[_df.iloc[:, 1] == 'Gross Domestic Product (GDP)']
    _df = _df.drop(_df.columns[:2], axis=1).transpose()
    df = DataFrame()
    df['us_to_world'] = _df.loc[:, 'United States'].div(_df.sum(axis=1))
    df.plot(grid=True)


if __name__ == '__main__':
    main()
