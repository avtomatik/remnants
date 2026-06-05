# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 23:12:03 2019

@author: Alexander Mikhailov
"""


import pandas as pd
from pandas.plotting import autocorrelation_plot

from core.classes import Dataset, SeriesID
from core.funcs import pull_by_series_id, stockpile


def main() -> None:
    SERIES_ID_CB = [SeriesID("D0086", Dataset.USCB)]
    SERIES_ID_LS = {
        "LNU04000000": "dataset_usa_bls-2017-07-06-ln.data.1.AllData"
    }

    df = pd.concat(
        [
            stockpile(SERIES_ID_CB),
            pd.concat(
                map(
                    lambda _: read_usa_bls(_[-1]).pipe(
                        pull_by_series_id, _[0]
                    ),
                    SERIES_ID_LS.items(),
                ),
                axis=1,
                sort=True,
            ).apply(pd.to_numeric, errors="coerce"),
        ],
        axis=1,
    )
    df.plot(title="US Unemployment, {}$-${}".format(*df.index[[0, -1]]))
    df.pipe(transform_mean, name="fused").pipe(autocorrelation_plot)


if __name__ == "__main__":
    main()
