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
