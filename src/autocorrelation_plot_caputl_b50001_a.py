#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 22:05:21 2023

@author: green-machine
"""


from pandas.plotting import autocorrelation_plot
from thesis.src.lib.read import read_usa_frb_g17


def main() -> None:
    {'source': 'http://www.federalreserve.gov/releases/g17/gvp.htm'}
    SERIES_ID = 'CAPUTL.B50001.A'
    read_usa_frb_g17().loc[:, (SERIES_ID,)].dropna(
        axis=0).pipe(autocorrelation_plot)


if __name__ == '__main__':
    main()
