import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import joblib
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import re


data = pd.read_json("data123.json")
data.columns = [
    re.sub(r'[^A-Za-z0-9_]+', '_', col)
    for col in data.columns
]
x = data.drop(columns=["id", "price"])
y = data["price"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
models = {
    "XGBoost": XGBRegressor(
        n_estimators=5000,
        max_depth=5,
        learning_rate=0.01,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=42
    ),

    "LightGBM": LGBMRegressor(
        n_estimators=5000,
        max_depth=-1,
        learning_rate=0.01,
        num_leaves=80,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )
}
results = []

for name, model in models.items():
    model.fit(x_train, y_train)

    pred = model.predict(x_test)

    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    mape = mean_absolute_percentage_error(y_test, pred)
    r2 = r2_score(y_test, pred)

    results.append({
        "model": name,
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "R2": r2
    })

results_df = pd.DataFrame(results).sort_values("MAE")
joblib.dump(models["XGBoost"], "model.pkl")
print(results_df)
results_df.to_json("model_score.json", orient="records", indent=2, force_ascii=False)
