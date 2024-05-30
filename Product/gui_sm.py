import streamlit as sl
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

sl.write("""
# NFL Season Record Predictor
""")

df = pd.read_csv("temp_onecopy.csv")

choice = sl.radio("Select an option", ["Year", "CSV"])
if choice == "Year":
    try:
        year = sl.text_input("Enter a year between 2003 and 2023", value=2023)
        year = int(year)
        if year < 2003 or year > 2023:
            sl.error("Enter a year between 2003 and 2023")
        
    except:
        sl.error("Please provide a valid type")
    df = pd.read_csv("temp_onecopy.csv")
    df = df[df["season"] == year]

else:
    file = sl.file_uploader(label="Upload a CSV")
    if file is not None:
        df = pd.read_csv(file)
    else:
        sl.write("Sample:")
    
    

display = pd.DataFrame(df["team"])

df = df.drop(columns=["season"])

answers = df["percent"].to_list()
df = df.drop(columns=["percent", "team"])

model = tf.keras.models.load_model("v1.keras")
model.load_weights("v1.h5")

stuff = model.predict(df.to_numpy()).flatten()
stuff = np.round(stuff, decimals=3)
pm = []

for i in range(len(stuff)):
    pm.append(str(round((abs(stuff.tolist()[i]-answers[i])/(1 if answers[i] == 0 else answers[i]))*100, 3)) + "%")

display.insert(len(display.columns), "Predictions", stuff)
display.insert(len(display.columns), "Answers", answers)
display.insert(len(display.columns), "% Uncertainity", pm)

display = display.set_index('team')

sl.table(display)