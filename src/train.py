import re
import json
import joblib
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, RandomizedSearchCV, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

data = pd.read_json("data123.json")

data.columns = [
    re.sub(r"[^A-Za-z0-9_]+", "_", col)
    for col in data.columns
]

X = data.drop(columns=["id", "price"])
y = data["price"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

cv = KFold(n_splits=5, shuffle=True, random_state=42)


models = {
    "LinearRegression": (
        LinearRegression(),
        {}
    ),

    "Ridge": (
        Ridge(),
        {
            "alpha": [0.1, 1.0, 10.0, 50.0, 100.0]
        }
    ),

    "RandomForest": (
        RandomForestRegressor(random_state=42),
        {
            "n_estimators": [200, 500, 1000],
            "max_depth": [None, 10, 20, 30],
            "min_samples_split": [2, 5, 10]
        }
    ),

    "GradientBoosting": (
        GradientBoostingRegressor(random_state=42),
        {
            "n_estimators": [200, 500, 1000],
            "learning_rate": [0.01, 0.05, 0.1],
            "max_depth": [3, 5, 8]
        }
    ),

    "XGBoost": (
        XGBRegressor(
            objective="reg:squarederror",
            random_state=42
        ),
        {
            "n_estimators": [500, 1000, 2000],
            "max_depth": [3, 5, 7],
            "learning_rate": [0.01, 0.03, 0.1],
            "subsample": [0.8, 1.0],
            "colsample_bytree": [0.8, 1.0]
        }
    ),

    "LightGBM": (
        LGBMRegressor(random_state=42),
        {
            "n_estimators": [500, 1000, 2000],
            "num_leaves": [31, 50, 80],
            "learning_rate": [0.01, 0.03, 0.1],
            "subsample": [0.8, 1.0],
            "colsample_bytree": [0.8, 1.0]
        }
    )
}

results = []
best_model = None
best_name = None
best_mae = float("inf")


for name, (model, params) in models.items():

    search = RandomizedSearchCV(
        estimator=model,
        param_distributions=params,
        n_iter=20 if params else 1,
        scoring="neg_mean_absolute_error",
        cv=cv,
        random_state=42,
        n_jobs=-1,
        verbose=0
    )

    search.fit(X_train, y_train)

    best_estimator = search.best_estimator_

    pred = best_estimator.predict(X_test)

    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)
    mape = mean_absolute_percentage_error(y_test, pred)

    results.append({
        "model": name,
        "best_params": search.best_params_,
        "MAE": float(mae),
        "RMSE": float(rmse),
        "R2": float(r2),
        "MAPE": float(mape)
    })

    if mae < best_mae:
        best_mae = mae
        best_model = best_estimator
        best_name = name
        best_cv_mae = -search.best_score_
        best_params = search.best_params_
        best_rmse = rmse
        best_r2 = r2
        best_mape = mape


joblib.dump(best_model, "model.pkl")


best_result = {
    "model": best_name,
    "best_params": best_params,

    "cross_validation": {
        "cv_folds": 5,
        "cv_metric": "MAE",
        "cv_mae": float(best_cv_mae)
    },

    "test_metrics": {
        "MAE": float(best_mae),
        "RMSE": float(best_rmse),
        "R2": float(best_r2),
        "MAPE": float(best_mape)
    }
}


with open("model_score.json", "w", encoding="utf-8") as f:
    json.dump(best_result, f, indent=2, ensure_ascii=False)