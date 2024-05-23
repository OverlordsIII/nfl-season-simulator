import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer as knn

df = pd.read_csv("temp.csv")

df = df.drop(["season"], axis=1)
df = df.drop(["team"], axis=1)


training_df = df.sample(frac=0.8, random_state=0)

training_features = pd.DataFrame(training_df).drop(['percent'], axis=1)
training_answers = training_df["percent"].to_list()

training_features = pd.DataFrame(knn(n_neighbors=5).fit_transform(training_features))
training_features = tf.convert_to_tensor(training_features)

normal = tf.keras.layers.Normalization(axis=-1)

model = tf.keras.Sequential([
    tf.keras.layers.Normalization(axis=-1, shape=training_features.shape),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(units=-1)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(training_features, training_answers, epochs=10)