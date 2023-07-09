#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 19:01:22 2023

@author: green-machine
"""


from core.funcs import calculate_curve_fit_params

# =============================================================================
# usa_cobb_douglas0013.py
# =============================================================================


if __name__ == '__main__':
    YEAR_BASE = 1899

    combine_cobb_douglas().pipe(
        transform_cobb_douglas, year_base=YEAR_BASE
    )[0].pipe(calculate_curve_fit_params)
