import streamlit as sl
import pandas as pd
import tensorflow as tf
from sklearn.impute import KNNImputer
from tensorflow import keras
import numpy as np
import os

def getModelPaths():
    models = []
    for file in os.listdir(".\\"):
        if file.endswith(".keras"):
            models.append(file)
    return models


sl.write("""
# NFL Season Record Predictor
""")

df = pd.read_csv("temp_onecopy.csv")

modelPaths = getModelPaths()
print(modelPaths)

modelChoice = sl.radio("Select the model you want to use", modelPaths)

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
    
df = df.set_index(["season", "team"])
temp = df.index
temp2 = df.columns
df = pd.DataFrame(columns=temp2, index=temp, data=KNNImputer(n_neighbors=5).fit_transform(df.to_numpy()))
df = df.reset_index()

display = pd.DataFrame(df["team"])

df = df.drop(columns=["season"])

answers = df["percent"].to_list()
df = df.drop(columns=["percent", "team"])

model = tf.keras.models.load_model(modelChoice)


stuff = model.predict(df.to_numpy()).flatten()
stuff = pd.Series(stuff).map(lambda x: round(x, 4)).to_numpy()
pm = []

for i in range(len(stuff)):
    pm.append(str(round(abs(stuff[i] - answers[i]), 4)))

display.insert(len(display.columns), "Predictions", stuff)
display.insert(len(display.columns), "Answers", answers)
display.insert(len(display.columns), "Difference", pm)

display = display.set_index('team')

sl.table(display)