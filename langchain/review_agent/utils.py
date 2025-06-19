import pandas as pd


def read_excel(path):
    df = pd.read_csv(path)
    print("df = ", df)
    return df
