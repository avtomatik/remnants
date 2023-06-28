
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 11:52:01 2022

@author: alexander
"""
from pandas import DataFrame


def strip_deflator(df: DataFrame, col_num: int) -> DataFrame:
    # =========================================================================
    # TODO: Test <df.pipe(price_inverse) == df.pct_change()>
    # =========================================================================
    return df.iloc[:, [col_num]].pct_change().dropna(axis=0)
