import os
import pandas as pd
import numpy as np
import json
import cv2
from pathlib import Path
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageOps
from torchvision import models, transforms
import torch
from sentence_transformers import SentenceTransformer
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
from pathlib import Path
import json
import pandas as pd

BASE_PATH = "data"
IMG_SIZE = (224, 224)
device = "cuda" if torch.cuda.is_available() else "cpu"
text_model = SentenceTransformer("all-MiniLM-L6-v2")
resnet = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
resnet.fc = torch.nn.Identity()  # убираем последний классификатор
resnet = resnet.to(device)
resnet.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def process_image(path, size=IMG_SIZE):
    img = Image.open(path).convert("RGB")

    img.thumbnail(size)

    new_img = Image.new("RGB", size, (0, 0, 0))
    x = (size[0] - img.width) // 2
    y = (size[1] - img.height) // 2
    new_img.paste(img, (x, y))

    arr = np.array(new_img) / 255.0
    arr = np.transpose(arr, (2, 0, 1))  # (C, H, W)

    return arr

# =====================
# обработка всех картинок объявления
# =====================
def process_ad_images(folder_path):
    folder = Path(folder_path)

    embeddings = []

    for file in sorted(folder.iterdir()):
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            try:
                img = Image.open(file).convert("RGB")
                img_tensor = transform(img).unsqueeze(0).to(device)

                with torch.no_grad():
                    emb = resnet(img_tensor)  # shape: (1, 512)

                embeddings.append(emb.cpu().numpy()[0])

            except Exception as e:
                print(f"Ошибка с картинкой {file}: {e}")

    if len(embeddings) == 0:
        return np.zeros(512)

    return np.mean(embeddings, axis=0)

def descriptionpreprocessing(text):
    if text is None or str(text).strip() == "":
        return np.zeros(384)

    embedding = text_model.encode(str(text))

    return embedding  # shape: (384,)

path = "data"

folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
rows = []
# print(folders)
i = 0
for folder in folders:
    path = Path("data") / folder / "data.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        data["id"] = folder
        data["description"]=descriptionpreprocessing(data["description"])
        # print(data["description"])
        # print(folder)

    folder_path = os.path.join(BASE_PATH, folder)
    # картинки
    images = process_ad_images(folder_path)
    images.reshape(-1)
    data["images"] = images  # 👈 добавляем массив
    print(i)
    i+=1


    rows.append(data)
df = pd.DataFrame(rows)
df2 = df[:1]
df2.to_json("datacolumns.json", orient="records", indent=2, force_ascii=False)

df["Suprafață totală"] = df["Suprafață totală"].str.extract(r"(\d+)").astype(float)
df["Suprafață locativă"] = df["Suprafață locativă"].str.extract(r"(\d+)").astype(float)
df["Suprafață bucătărie"] = df["Suprafață bucătărie"].str.extract(r"(\d+)").astype(float)
df["Inălțimea tavanelor"] = df["Inălțimea tavanelor"].str.extract(r"(\d+)").astype(float)
df["Etaj"] = df["Etaj"].replace({
    "Penthouse": "1",
    "Subsol": "1",
    "Demisol": "0",
    np.nan : 0
})
df["Grup sanitar"] = df["Grup sanitar"].replace({
    "4 și mai multe": "4",
    np.nan : 0
})
df["Balcon/ lojie"] = df["Balcon/ lojie"].replace({
    "4 și mai multe": "4",
    np.nan : 0,
    "Nu" : 0
})

cols = ["Număr de etaje", "Etaj", "Grup sanitar", "Balcon/ lojie", "price", "lat", "long"]
df[cols] = df[cols].apply(pd.to_numeric, errors="coerce")
df[cols] = df[cols].fillna(0)
df["Număr de camere"] = (
    df["Număr de camere"]
    .str.extract(r"(\d+)")
    .astype("float")   # сначала float (из-за NaN)
    .astype("Int64")   # nullable int
)
num_cols = df.select_dtypes(include="number").columns
df[num_cols] = df[num_cols].fillna(0)
df = df.join(pd.DataFrame(df["images"].tolist()).add_prefix("images_"))
df = df.join(pd.DataFrame(df["description"].tolist()).add_prefix("description_"))
df = df.drop(columns=["description", "images"])


df = pd.get_dummies(
    df,
    columns=["Autorul anunțului", "Living", "Fond locativ", "Dezvoltator", "Starea apartamentului", "Compartimentare", "Loc de parcare", "Tip clădire", "Copii", "Animale"],
    drop_first=False,   # keeps e.g. smokes_yes and gender_M (or similar)
    dtype=int
)

df.to_json("data123.json", orient="records", indent=2, force_ascii=False)
df[:1].to_json("datacolumnsfin.json", orient="records", indent=2, force_ascii=False)