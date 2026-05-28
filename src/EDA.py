import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# загрузка
df = pd.read_json("data123.json")

# только числовые колонки
corr = df.select_dtypes(include=["number"]).corr()

# график
fig, ax = plt.subplots(figsize=(20, 20))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    ax=ax
)

plt.tight_layout()

# показать окно
plt.show()

# сохранить в файл
fig.savefig("correlation_heatmap.png", dpi=300)