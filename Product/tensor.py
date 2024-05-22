import tensorflow as tf
import pandas as pd

df = pd.read_csv("temp.csv")

df = df.drop(["season"], axis=1)
df = df.drop(["team"], axis=1)

training_df = df.sample(frac=0.8, random_state=0)

training_features = training_df
training_answers = training_df.["percent"].to_list()

