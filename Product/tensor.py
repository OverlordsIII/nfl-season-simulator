import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer as knn

df = pd.read_csv("temp.csv")
df = df.drop(["season"], axis=1)
df = df.drop(["team"], axis=1)
df.dropna(inplace=True, axis="index")
df.dropna(inplace=True, axis="columns")

df = df.sample(frac=1).reset_index(drop=True)

training_df = df.head(-(int(0.2*len(df))))
testing_df = df.tail(int(0.2*len(df)))

training_features = training_df.drop(['percent'], axis=1)
training_answers = training_df["percent"].to_list()

testing_features = testing_df.drop(["percent"], axis=1)
testing_answers = testing_df["percent"].to_list()

normal = tf.keras.layers.Normalization(axis=-1)
normal.adapt(np.array(training_features))

model = tf.keras.Sequential([
    normal,
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dense(1024, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['mean_absolute_error'])

model.fit(np.array(training_features), np.array(training_answers), epochs=40)

testing = pd.DataFrame()

testing["predicted"] = pd.Series(model.predict(np.array(testing_features)).flatten())
testing["actual"] = pd.Series(testing_answers)

resultsarr = np.array([])

for index, row in testing.iterrows():
    resultsarr = np.append(resultsarr, (abs(row["predicted"]-row["actual"])/row["actual"]))

print(resultsarr)
print("Results!")
print(np.average(resultsarr) * 100)
testing.to_csv("results.csv")

model.save("v1.keras")