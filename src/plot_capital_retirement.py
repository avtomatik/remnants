# =============================================================================
# projectCapitalRetirement.py
# =============================================================================


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame


def plot_capital_acquisition(period, investment, manufacturing, manufacturing_n, manufacturing_m, capital, labor):
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
    Y01 = manufacturing/capital
    # =========================================================================
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    # =========================================================================
    Y02 = investment*manufacturing[0]/(investment[0]*manufacturing)
    # =========================================================================
    # Labor Capital Intensity
    # =========================================================================
    Y03 = capital*labor[0]/(capital[0]*labor)
    # =========================================================================
    # Labor Productivity
    # =========================================================================
    Y04 = manufacturing*labor[0] / (manufacturing[0]*labor)
    # =========================================================================
    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    # =========================================================================
    Y05 = np.log(Y03)
    # =========================================================================
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    # =========================================================================
    Y06 = np.log(Y04)
    # =========================================================================
    # Max: Fixed Assets Turnover Ratio
    # =========================================================================
    Y07 = manufacturing_m/capital
    # =========================================================================
    # Max: Investment to Gross Domestic Product Ratio
    # =========================================================================
    Y08 = investment*manufacturing_m[0]/(investment[0]*manufacturing_m)
    # =========================================================================
    # Max: Labor Productivity
    # =========================================================================
    Y09 = manufacturing_m*labor[0]/(manufacturing_m[0]*labor)
    # =========================================================================
    # Max: Log Labor Productivity
    # =========================================================================
    Y10 = np.log(Y09)
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    Y05 = DataFrame(Y05, columns=['Y05'])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    Y06 = DataFrame(Y06, columns=['Y06'])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    Y10 = DataFrame(Y10, columns=['Y10'])
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
    _knots.append(0)
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
                    0, period[0])))
                if y > _knots[i]:
                    _knots.append(y)
                    pi.append(float(input('Define Pi for Period from {} to {}: '.format(
                        period[_knots[i]], period[_knots[1+i]]))))
                    i += 1
    else:
        print("Error")
    Y11 = []
    for i in range(1+0):
        Y11.append(np.nan)
    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1+j]):
            # =========================================================================
            # Estimate: GCF[-] or CA[+]
            # =========================================================================
            Y11.append(capital[1+i]-capital[i]+pi[j]*investment[1+i])
    else:
        for j in range(N):
            if j == N-1:
                for i in range(_knots[j], _knots[1+j]):
                    # =========================================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================================
                    Y11.append(capital[1+i]-capital[i] +
                               pi[j]*investment[1+i])
            else:
                for i in range(_knots[j], _knots[1+j]):
                    # =========================================================================
                    # Estimate: GCF[-] or CA[+]
                    # =========================================================================
                    Y11.append(capital[1+i]-capital[i] +
                               pi[j]*investment[1+i])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    Y11 = DataFrame(Y11, columns=['Y11'])
    df = DataFrame(period, columns=['period'])
    df = pd.concat([df, Y01, Y02, Y03, Y04, Y05, Y06,
                   Y07, Y08, Y09, Y10, Y11], axis=1)
    df.columns = ['period', 'Y01', 'Y02', 'Y03',
                  'Y04', 'Y05', 'Y06', 'Y07', 'Y08', 'Y09', 'Y10', 'Y11']
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
    plt.plot(Y03, Y04)
    plt.plot(Y03, Y09)
    plt.title('Labor Productivity, Observed & Max, %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]-1]))
    plt.xlabel('Labor Capital Intensity')
    plt.ylabel(f'Labor Productivity, {period[year_base]}=100')
    plt.grid()
    plt.figure(2)
    plt.plot(Y05, Y06)
    plt.plot(Y05, Y10)
    plt.title('Log Labor Productivity, Observed & Max, %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]-1]))
    plt.xlabel('Log Labor Capital Intensity')
    plt.ylabel(f'Log Labor Productivity, {period[year_base]}=100')
    plt.grid()
    plt.figure(3)
    plt.plot(Y01)
    plt.plot(Y07)
    plt.title('Fixed Assets Turnover, Observed & Max, %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]-1]))
    plt.xlabel('Period')
    plt.ylabel(f'Fixed Assets Turnover, {period[year_base]}=100')
    plt.grid()
    plt.figure(4)
    plt.plot(Y02)
    plt.plot(Y08)
    plt.title('Investment to Gross Domestic Product Ratio,\nObserved & Max, %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel(f'Investment to GDP Ratio, {period[year_base]}=100')
    plt.grid()
    plt.figure(5)
    plt.plot(Y11)
    plt.title('Gross Capital Formation (GCF) or\nCapital Acquisitions (CA), %d=100, {}$-${}'.format(
        period[year_base], period[_knots[0]], period[_knots[N]-1]))
    plt.xlabel('Period')
    plt.ylabel(f'GCF or CA, {period[year_base]}=100')
    plt.grid()
    plt.show()


def plot_capital_retirement(period, investment, manufacturing, manufacturing_n, capital, labor):
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
    pi, _knots = [], [0, ]
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
    plt.title('Investment to GDP Ratio, %d=100, {}$-${}'.format(
        period[year_base], period[0], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel(f'Investment to GDP Ratio, {period[year_base]}=100')
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
