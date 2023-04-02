#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 13:27:12 2023

@author: green-machine
"""


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lib.tools import collect_capital_combined_archived
from pandas import DataFrame

# =============================================================================
# projectCapitalAcquisitions.py
# =============================================================================
'''Project: Capital Acquisitions'''
# =============================================================================
# capital_acquisitions.yaml
# =============================================================================


def plot_capital_acquisition(period, investment, manufacturing, manufacturing_n, manufacturing_m, capital, labor, start):
    i = len(period)-1
    while abs(manufacturing_n[i]-manufacturing[i]) > 1:
        i -= 1
        # =========================================================================
        # Basic Year
        # =========================================================================
        year_base = i

    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    X01 = manufacturing/capital

    # =========================================================================
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    # =========================================================================
    X02 = investment*manufacturing[start]/(investment[start]*manufacturing)
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    X03 = capital*labor[start]/(capital[start]*labor)
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    X04 = manufacturing*labor[start] / (manufacturing[start]*labor)
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    # =========================================================================
    X05 = np.log(X03)
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    # =========================================================================
    X06 = np.log(X04)
    # =========================================================================
    # Max: Fixed Assets Turnover Ratio
    # =========================================================================
    X07 = manufacturing_m/capital

    # =========================================================================
    # Max: Investment to Gross Domestic Product Ratio
    # =========================================================================
    X08 = investment*manufacturing_m[start]/(investment[start]*manufacturing_m)
    # =========================================================================
    # Max: Labor Productivity
    # =========================================================================
    X09 = manufacturing_m*labor[start]/(manufacturing_m[start]*labor)
    # =========================================================================
    # Max: Log Labor Productivity
    # =========================================================================
    X10 = np.log(X09)
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    X05 = DataFrame(X05, columns=['X05'])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    X06 = DataFrame(X06, columns=['X06'])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    X10 = DataFrame(X10, columns=['X10'])
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Line Segments for Pi: '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 1, f'N >= 1 is Required, N = {N} Was Provided'
    # =========================================================================
    # Pi & Pi Switch Points
    # =========================================================================
    pi, _knots = [], []
    _knots.append(start)
    i = 0
    if N == 1:
        _knots.append(len(period)-1)
        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
            period[_knots[i]], period[_knots[1+i]-1]))))
    elif N >= 2:
        while i < N:
            if i == N-1:
                _knots.append(len(period)-1)
                pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                    period[_knots[i]], period[_knots[1+i]-1]))))
                i += 1
            else:
                y = int(input('Select Row for Year, Should Be More Than %d:=%d: ' % (
                    start, period[start])))
                if y > _knots[i]:
                    _knots.append(y)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        period[_knots[i]], period[_knots[1+i]]))))
                    i += 1
    else:
        print("Error")
    X11 = []
    for i in range(1+start):
        X11.append(np.nan)
    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1+j]):
            # =========================================================================
            # Estimate: GCF[-] or CA[+]
            # =========================================================================
            X11.append(capital[1+i]-capital[i]+pi[j]*investment[1+i])
    else:
        for j in range(N):
            if j == N-1:
                for i in range(_knots[j], _knots[1+j]):
                    # =========================================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================================
                    X11.append(capital[1+i]-capital[i] +
                               pi[j]*investment[1+i])
            else:
                for i in range(_knots[j], _knots[1+j]):
                    # =========================================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================================
                    X11.append(capital[1+i]-capital[i] +
                               pi[j]*investment[1+i])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    X11 = DataFrame(X11, columns=['X11'])
    df = DataFrame(period, columns=['period'])
    df = pd.concat([df, X01, X02, X03, X04, X05, X06,
                   X07, X08, X09, X10, X11], axis=1)
    df.columns = ['period', 'X01', 'X02', 'X03',
                  'X04', 'X05', 'X06', 'X07', 'X08', 'X09', 'X10', 'X11']
    # [-] Gross Capital Formation
    # [+] Capital Acquisitions
    for i in range(N):
        if i == N-1:
            print('Model Parameter: Pi for Period from %d to %d: %f' %
                  (period[_knots[i]], period[_knots[1+i]-1], pi[i]))
        else:
            print('Model Parameter: Pi for Period from %d to %d: %f' %
                  (period[_knots[i]], period[_knots[1+i]], pi[i]))
        plt.figure(1)
    plt.plot(X03, X04)
    plt.plot(X03, X09)
    plt.title('Labor Productivity, Observed & Max, %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel(f'Labor Productivity, {period[year_base]}=100')
    plt.grid()
    plt.figure(2)
    plt.plot(X05, X06)
    plt.plot(X05, X10)
    plt.title('Log Labor Productivity, Observed & Max, %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]-1]))
    plt.xlabel('Log Labor Capital Intensity')
    plt.ylabel(f'Log Labor Productivity, {period[year_base]}=100')
    plt.grid()
    plt.figure(3)
    plt.plot(X01)
    plt.plot(X07)
    plt.title('Fixed Assets Turnover, Observed & Max, %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]-1]))
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover, {period[year_base]}=100')
    plt.grid()
    plt.figure(4)
    plt.plot(X02)
    plt.plot(X08)
    plt.title('Investment to Gross Domestic Product Ratio,\nObserved & Max, %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel('Investment to Gross Domestic Product Ratio, %d=100' %
               (period[year_base]))
    plt.grid()
    plt.figure(5)
    plt.plot(X11)
    plt.title('Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]-1]))
    plt.xlabel('Period')
    plt.ylabel(f'GCF or CA, {period[year_base]}=100')
    plt.grid()
    plt.show()


def transform_call(df, start):
    _df = df.dropna()
    # =========================================================================
    # Investment
    # =========================================================================
    I = _df.iloc[:, 1].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    # =========================================================================
    # Product
    # =========================================================================
    Y = _df.iloc[:, 3]
    YN = _df.iloc[:, 2]
    # =========================================================================
    # Max: Product
    # =========================================================================
    YM = _df.iloc[:, 3].div(_df.iloc[:, 4]).mul(100)
    # =========================================================================
    # Fixed Assets, End-Period, Not Adjusted
    # =========================================================================
    C = _df.iloc[:, 6].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    L = _df.iloc[:, 7]
    plot_capital_acquisition(I, Y, YN, YM, C, L, start)


# =============================================================================
# 1967
# =============================================================================
# start = 38
collect_capital_combined_archived().pipe(transform_call, start=38)
# =============================================================================
# projectCapitalRetirement.py
# =============================================================================


def plot_capital_retirement(period, investment, manufacturing, manufacturing_n, capital, labor):
    # =========================================================================
    # Y05.append(capital[1+i]-capital[i]+gmm[j]*investment[1+i])
    # =========================================================================
    # =========================================================================
    # Y06.append((capital[1+i]-capital[i]+gmm[j]*investment[1+i])/capital[1+i])
    # =========================================================================
    # =========================================================================
    # Replaced with
    # =========================================================================
    # =========================================================================
    # Y05.append(capital[i]-capital[1+i]+gmm[j]*investment[i])
    # =========================================================================
    # =========================================================================
    # Y06.append((capital[i]-capital[1+i]+gmm[j]*investment[i])/capital[1+i])
    # =========================================================================
    # =========================================================================
    # Define Basic Year for Deflator
    # =========================================================================
    i = len(period)-1
    while abs(manufacturing_n[i]-manufacturing[i]) > 1:
        i -= 1
        # =========================================================================
        # Basic Year
        # =========================================================================
        year_base = i

    # =========================================================================
    # Calculate Static Values
    # =========================================================================
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    # =========================================================================
    Y01 = np.log(capital*labor[0]/(capital[0]*labor))
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    # =========================================================================
    Y02 = np.log(manufacturing*labor[0]/(manufacturing[0]*labor))
    # =========================================================================
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    # =========================================================================
    Y03 = investment*manufacturing[0]/(investment[0]*manufacturing)
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    Y04 = manufacturing/capital

    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    Y01 = DataFrame(Y01, columns=['Y01'])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    Y02 = DataFrame(Y02, columns=['Y02'])
    # =========================================================================
    # Number of Spans
    # =========================================================================
    N = int(input('Define Number of Line Segments for Pi: '))
    print(f'Number of Spans Provided: {N}')
    assert N >= 1, f'N >= 1 is Required, N = {N} Was Provided'
    # =========================================================================
    # Pi & Pi Switch Points
    # =========================================================================
    pi, _knots = [], []
    _knots.append(0)
    i = 0
    if N == 1:
        _knots.append(len(period)-1)
        pi.append(float(input('Define Pi for Period from {} to {}: '.format(
            period[_knots[i]], period[_knots[1+i]]))))
    elif N >= 2:
        while i < N:
            if i == N-1:
                _knots.append(len(period)-1)
                pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                    period[_knots[i]], period[_knots[1+i]]))))
                i += 1
            else:
                y = int(input('Select Row for Year: '))
                if y > _knots[i]:
                    _knots.append(y)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        period[_knots[i]], period[_knots[1+i]]))))
                    i += 1
    else:
        print("Error")
    Y05 = []
    Y06 = []
    # =========================================================================
    # Fixed Assets Retirement Value
    # =========================================================================
    Y05.append(np.nan)
    # =========================================================================
    # Fixed Assets Retirement Ratio
    # =========================================================================
    Y06.append(np.nan)
    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================
    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1+j]):
            # =========================================================================
            # Fixed Assets Retirement Value
            # =========================================================================
            Y05.append(capital[i]-capital[1+i]+pi[j]*investment[i])
            # =========================================================================
            # Fixed Assets Retirement Ratio
            # =========================================================================
            Y06.append((capital[i]-capital[1+i]+pi[j]
                       * investment[i])/capital[1+i])
    else:
        for j in range(N):
            if j == N-1:
                for i in range(_knots[j], _knots[1+j]):
                    # =========================================================================
                    # Fixed Assets Retirement Value
                    # =========================================================================
                    Y05.append(capital[i]-capital[1+i] +
                               pi[j]*investment[i])
                    # =========================================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================================
                    Y06.append(
                        (capital[i]-capital[1+i]+pi[j]*investment[i])/capital[1+i])
            else:
                for i in range(_knots[j], _knots[1+j]):
                    # =========================================================================
                    # Fixed Assets Retirement Value
                    # =========================================================================
                    Y05.append(capital[i]-capital[1+i] +
                               pi[j]*investment[i])
                    # =========================================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================================
                    Y06.append(
                        (capital[i]-capital[1+i]+pi[j]*investment[i])/capital[1+i])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    Y05 = DataFrame(Y05, columns=['Y05'])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    Y06 = DataFrame(Y06, columns=['Y06'])
    df = DataFrame(period, columns=['period'])
    df = pd.concat([df, Y01, Y02, Y03, Y04, Y05, Y06], axis=1)
    df.columns = ('period', 'Y01', 'Y02', 'Y03', 'Y04', 'Y05', 'Y06')
    df['Y07'] = df['Y06']-df['Y06'].mean()
    df['Y07'] = df['Y07'].abs()
    df['Y08'] = df['Y06'].diff()
    df['Y08'] = df['Y08'].abs()
    for i in range(N):
        if i == N-1:
            print('Model Parameter: Pi for Period from %d to %d: %f' %
                  (period[_knots[i]], period[_knots[1+i]], pi[i]))
        else:
            print('Model Parameter: Pi for Period from %d to %d: %f' %
                  (period[_knots[i]], period[_knots[1+i]], pi[i]))
        plt.figure(1)
    plt.title(
        'Product, %d=100, {}$-${}'.format(period[year_base], period[0], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel(f'Product, {period[year_base]}=100')
    plt.plot(manufacturing)
    plt.grid()
    plt.figure(2)
    plt.title(
        'Capital, %d=100, {}$-${}'.format(period[year_base], period[0], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel(f'Capital, {period[year_base]}=100')
    plt.plot(capital)
    plt.grid()
    plt.figure(3)
    plt.title(
        'Fixed Assets Turnover, %d=100, {}$-${}'.format(period[year_base], period[0], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover, {period[year_base]}=100')
    plt.plot(manufacturing/capital)
    plt.grid()
    plt.figure(4)
    plt.title('Investment to Gross Domestic Product Ratio, %d=100, {}$-${}'.format(
        period[year_base], period[0], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel('Investment to Gross Domestic Product Ratio, %d=100' %
               (period[year_base]))
    plt.plot(Y03)
    plt.grid()
    plt.figure(5)
    plt.title('$\\mu(t)$, Fixed Assets Retirement Ratio, %d=100, {}$-${}'.format(
        period[year_base], period[0], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel(f'$\\mu(t)$, {period[year_base]}=100')
    plt.plot(Y06)
    plt.grid()
    plt.figure(6)
    plt.title('Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, %d=100, {}$-${}'.format(
        period[year_base], period[0], period[_knots[N]]))
    plt.xlabel(f'$\\mu(t)$, {period[year_base]}=100')
    plt.ylabel(f'Fixed Assets Retirement Value, {period[year_base]}=100')
    plt.plot(Y06, Y05)
    plt.grid()
    plt.figure(7)
    plt.title(
        'Labor Capital Intensity, %d=100, {}$-${}'.format(period[year_base], period[0], period[_knots[N]]))
    plt.xlabel(f'Labor Capital Intensity, {period[year_base]}=100')
    plt.ylabel(f'Labor Productivity, {period[year_base]}=100')
    plt.plot(np.exp(Y01), np.exp(Y02))
    # plt.legend()
    plt.grid()
    plt.show()

# =============================================================================
# Data Fetch: Run 'projectCapital.py'
# =============================================================================


kwargs = {
    'filepath_or_buffer': 'archive project CapitalAcquisitionsRetirement.csv',
    'skiprows': range(1, 23)
}
df = pd.read_csv(**kwargs)
df['period'] = df['period'].astype(int)
# =============================================================================
# capital_retirement.yaml
# =============================================================================
T = df.iloc[:, 0]
# =============================================================================
# Investment
# =============================================================================
I = df.iloc[:, 1].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
# =============================================================================
# Product
# =============================================================================
Y = df.iloc[:, 3]
YN = df.iloc[:, 2]
# =============================================================================
# Max: Product
# =============================================================================
# YM = df.iloc[:, 3].div(df.iloc[:, 4]).div(100)
# Fixed Assets, End-Period, Not Adjusted
C = df.iloc[:, 6].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
L = df.iloc[:, 7]
# =============================================================================
# C = df.iloc[:, 5].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
# =============================================================================
# =============================================================================
# L = df.iloc[:, 8]
# =============================================================================
# =============================================================================
# Replaced with
# =============================================================================
# =============================================================================
# C = df.iloc[:, 6].mul(df.iloc[:, 3]).div(df.iloc[:, 2])
# =============================================================================
# =============================================================================
# L = df.iloc[:, 7]
# =============================================================================

plot_capital_retirement(I, Y, YN, C, L)
