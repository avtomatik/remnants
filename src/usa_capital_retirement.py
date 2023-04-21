'''Project: Capital Retirement'''
# =============================================================================
# capital_retirement.yaml
# =============================================================================
from itertools import product

from remnants.src.lib.combine import combine_capital_combined_archived
from remnants.src.plot_capital_retirement import plot_capital_retirement


def main(df):
    # df = combine_local().pipe(transform_local)
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

df = combine_capital_combined_archived()

if __name__ == '__main__':
    main(df, 38, 83)
