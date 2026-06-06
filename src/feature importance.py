import joblib
from xgboost import plot_importance
import matplotlib.pyplot as plt

model = joblib.load("model.pkl")
fig, ax = plt.subplots(figsize=(12, 8))

plot_importance(
    model,
    max_num_features=50,
    ax=ax
)

plt.tight_layout()

fig.savefig(
    "xgboost_feature_importance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)