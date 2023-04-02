'''Project: Capital Retirement'''
# =============================================================================
# capital_retirement.yaml
# =============================================================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lib.tools import collect_capital_combined_archived
from pandas import DataFrame


def plot_capital_retirement(period, investment, manufacturing, manufacturing_n, capital, labor):

    i = len(period)-1
    # if manufacturing==YM:

    while abs(manufacturing_n[i]-manufacturing[i]) > 1:
        i -= 1
        # =========================================================================
        # Basic Year
        # =========================================================================
        year_base = i

    # =========================================================================
    # Calculate Static Values
    # =========================================================================

    # Log Labor Capital Intensity, LN((K/L)/(K0/L0))
    X01 = np.log(capital*labor[0]/(capital[0]*labor))
    # Log Labor Productivity, LN((Y/L)/(Y0/L0))
    X02 = np.log(manufacturing*labor[0]/(manufacturing[0]*labor))
    # Investment to Gross Domestic Product Ratio, (I/Y)/(I0/Y0)
    X03 = investment*manufacturing[0]/(investment[0]*manufacturing)
    # =========================================================================
    # Fixed Assets Turnover Ratio
    # =========================================================================
    X04 = manufacturing/capital

    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    X01 = DataFrame(X01, columns=['X01'])

    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    X02 = DataFrame(X02, columns=['X02'])

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
    X05 = []
    X06 = []
    # =========================================================================
    # Fixed Assets Retirement Value
    # =========================================================================
    X05.append(np.nan)

    # =========================================================================
    # Fixed Assets Retirement Ratio
    # =========================================================================
    X06.append(np.nan)

    # =========================================================================
    # Calculate Dynamic Values
    # =========================================================================

    if N == 1:
        j = 0
        for i in range(_knots[j], _knots[1+j]):
            # =========================================================================
            # Fixed Assets Retirement Value
            # =========================================================================

            X05.append(capital[i]-capital[1+i]+pi[j]*investment[i])
            # =========================================================================
            # Fixed Assets Retirement Ratio
            # =========================================================================

            X06.append((capital[i]-capital[1+i]+pi[j]
                        * investment[i])/capital[1+i])
    else:
        for j in range(N):
            if j == N-1:
                for i in range(_knots[j], _knots[1+j]):
                    # =========================================================================
                    # Fixed Assets Retirement Value
                    # =========================================================================

                    X05.append(capital[i]-capital[1+i] +
                               pi[j]*investment[i])
                    # =========================================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================================

                    X06.append(
                        (capital[i]-capital[1+i]+pi[j]*investment[i])/capital[1+i])
            else:
                for i in range(_knots[j], _knots[1+j]):
                    # =========================================================================
                    # Fixed Assets Retirement Value
                    # =========================================================================

                    X05.append(capital[i]-capital[1+i] +
                               pi[j]*investment[i])
                    # =========================================================================
                    # Fixed Assets Retirement Ratio
                    # =========================================================================

                    X06.append(
                        (capital[i]-capital[1+i]+pi[j]*investment[i])/capital[1+i])
    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    X05 = DataFrame(X05, columns=['X05'])

    # =========================================================================
    # Convert List to DataFrame
    # =========================================================================
    X06 = DataFrame(X06, columns=['X06'])

    df = DataFrame(period, columns=['period'])
    df = pd.concat([df, X01, X02, X03, X04, X05, X06], axis=1)
    df.columns = ['period', 'X01',
                  'X02', 'X03', 'X04', 'X05', 'X06']
    df['X07'] = df['X06']-df['X06'].mean()
    df['X07'] = df['X07'].abs()
    df['X08'] = df['X06'].diff()
    df['X08'] = df['X08'].abs()
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
    plt.title(
        'Investment to GDP Ratio, %d=100, {}$-${}'.format(period[year_base], period[0], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel(f'Investment to GDP Ratio, {period[year_base]}=100')
    plt.plot(X03)
    plt.grid()
    plt.figure(5)
    plt.title('$\\mu(t)$, Fixed Assets Retirement Ratio, %d=100, {}$-${}'.format(
        period[year_base], period[0], period[_knots[N]]))
    plt.xlabel('Period')
    plt.ylabel(f'$\\mu(t)$, {period[year_base]}=100')
    plt.plot(X06)
    plt.grid()
    plt.figure(6)
    plt.title('Fixed Assets Retirement Ratio to Fixed Assets Retirement Value, %d=100, {}$-${}'.format(
        period[year_base], period[0], period[_knots[N]]))
    plt.xlabel(f'$\\mu(t)$, {period[year_base]}=100')
    plt.ylabel(f'Fixed Assets Retirement Value, {period[year_base]}=100')
    plt.plot(X06, X05)
    plt.grid()
    plt.figure(7)
    plt.title(
        'Labor Capital Intensity, %d=100, {}$-${}'.format(period[year_base], period[0], period[_knots[N]]))
    plt.xlabel(f'Labor Capital Intensity, {period[year_base]}=100')
    plt.ylabel(f'Labor Productivity, {period[year_base]}=100')
    plt.plot(np.exp(X01), np.exp(X02))
    plt.grid()
    # plt.legend()
    plt.show()



def main(df, start, stop):
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
    YM = _df.iloc[:, 3].mul(100).div(_df.iloc[:, 4])
    # =========================================================================
    # Capital, End-Period, Not Adjusted
    # =========================================================================
    C = _df.iloc[:, 6].mul(_df.iloc[:, 3]).div(_df.iloc[:, 2])
    L = _df.iloc[:, 7]
    plot_capital_retirement(I, Y, YN, C, L)
    plot_capital_retirement(I, YM, YN, C, L)


STARTS = {22: 1951, 38: 1967}
STOPS = {83: 2011}
BOUNDS = tuple(product(STARTS, STOPS))

df = collect_capital_combined_archived()

if __name__ == '__main__':
    main(df, 38, 83)
