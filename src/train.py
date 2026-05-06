import pandas as pd
import json
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error
import joblib



data = pd.read_json("data123.json")[:10000]

x = data.drop(columns=["id", "price"])
y = data["price"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
lr_perfect = make_pipeline(StandardScaler(), LinearRegression())
# # lr_perfect = LinearRegression()
lr_perfect.fit(x_train, y_train)
# # lr_perfect.fit(x, y)
joblib.dump(lr_perfect, "model.pkl")

model = joblib.load("model.pkl")
y_pred = abs(model.predict(x_test))
meanerror = mean_absolute_percentage_error(y_test, y_pred)
print(meanerror)
meanerror = mean_absolute_error(y_test, y_pred)
print(meanerror)
# print(y_pred)
# print(data)