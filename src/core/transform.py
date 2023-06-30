from core.strings.funcs import trim_string
from pandas import DataFrame


def filter_data_frame(df: DataFrame, query: dict[str]) -> DataFrame:
    for column, criterion in query['filter'].items():
        df = df[df.iloc[:, column] == criterion]
    return df


def transform_sub_sum(df: DataFrame) -> DataFrame:
    df["delta"] = df.iloc[:, 0].sub(df.iloc[:, 1:].sum(axis=1))
    return df


def transform_sub_special(df: DataFrame) -> DataFrame:
    # =========================================================================
    # df['delta_eq'] = df.iloc[:, 0].sub(df.iloc[:, -1])
    # =========================================================================
    df['delta_eq'] = df.iloc[:, 0].mul(4).div(
        df.iloc[:, 0].add(df.iloc[:, -1])).sub(2)
    return df


def transform_usa_macroeconomics(df: DataFrame) -> DataFrame:
    df.loc[:, 'A191RD'] = df.loc[:, 'A191RD'].rdiv(100)
    return df


def trim_columns(df: DataFrame) -> DataFrame:
    df.columns = map(lambda _: trim_string(_, fill='_').lower(), df.columns)
    return df


def transform_usa_bls_cpiu(df: DataFrame) -> DataFrame:
    df.rename_axis('period', inplace=True)
    df['mean'] = df.mean(axis=1)
    df['sqrt'] = df.iloc[:, :-1].prod(1).pow(1 / 12)
    # =========================================================================
    # Tests
    # =========================================================================
    df['mean_less_sqrt'] = df.iloc[:, -2].sub(df.iloc[:, -1])
    df['dec_on_dec'] = df.iloc[:, -3].pct_change()
    df['mean_on_mean'] = df.iloc[:, -4].pct_change()
    return df.iloc[:, [-1]].dropna(axis=0)
