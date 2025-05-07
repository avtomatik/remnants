# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 23:12:03 2019

@author: Alexander Mikhailov
"""


import os

import matplotlib.pyplot as plt
import pandas as pd
from core.config import BASE_DIR, DATA_DIR
from core.funcs import pull_by_series_id, stockpile, transform_mean
from pandas.plotting import autocorrelation_plot
from thesis.src.lib.read import read_usa_bls


def main(
    savefig: bool = False,
    file_name: str = 'plot_usa_unemployment_autocorrelation.pdf'
) -> None:
    SERIES_ID_CB = [SeriesID('D0086', Dataset.USCB)]
    SERIES_ID_LS = {
        'LNU04000000': 'dataset_usa_bls-2017-07-06-ln.data.1.AllData'
    }

    os.chdir(BASE_DIR)

    df = pd.concat(
        [
            stockpile(SERIES_ID_CB),
            pd.concat(
                map(
                    lambda _: read_usa_bls(_[-1]).pipe(
                        pull_by_series_id, _[0]
                    ),
                    SERIES_ID_LS.items()
                ),
                axis=1,
                sort=True
            ).apply(pd.to_numeric, errors='coerce'),
        ],
        axis=1
    )
    df.plot(title='US Unemployment, {}$-${}'.format(*df.index[[0, -1]]))
    df.pipe(transform_mean, name="fused").pipe(autocorrelation_plot)

    if savefig:
        plt.savefig(DATA_DIR.joinpath(file_name), format='pdf', dpi=900)


if __name__ == '__main__':
    main()
