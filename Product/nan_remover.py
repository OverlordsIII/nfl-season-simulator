import pandas as pd
import numpy as np


def remove_nans(df):
  df = pd.read_csv("temp2024w4.csv")
  df.replace(np.nan, '0', inplace=True)

  return df