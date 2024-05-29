import streamlit as sl
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

sl.write("""
# NFL Season Record Predictor
""")

# week = sl.selectbox(
#     "Select a week",
#     tuple([i+1 for i in list(range(2, 17))])
# )

year = sl.text_input("Enter a year between 2003 and 2023", value=2023)


try:
    year = int(year)
    if year < 2003 or year > 2023:
        sl.error("Enter a year between 2003 and 2023")
    
except:
    sl.error("Please provide a valid type")

df = pd.read_csv("temp.csv")
df = df[df["season"] == year]



display = pd.DataFrame(df["team"])

df = df.drop(columns=["season"])

answers = df["percent"].to_list()
df = df.drop(columns=["percent", "team"])

model = tf.keras.models.load_model("v1.keras")

stuff = model.predict(df.to_numpy()).flatten()
stuff = np.round(stuff, decimals=3)

display.insert(len(display.columns), "Predictions", stuff)
display.insert(len(display.columns), "Answers", answers)

display = display.set_index('team')

sl.table(display)