import pandas as pd


def convert_to_dataframe(data, columns):
    return pd.DataFrame(
        data,
        columns=columns
    )