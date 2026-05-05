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
import joblib
import os
import json
import cv2
from pathlib import Path
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer, WordNetLemmatizer
import string
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
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


def main():
    data1 = pd.read_json("datacolumns.json")[:1]
    text_model = SentenceTransformer("all-MiniLM-L6-v2")
    BASE_PATH = "data"
    IMG_SIZE = (224, 224)
    device = "cuda" if torch.cuda.is_available() else "cpu"

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

    rows = []
    path = Path("querry") / "data.json"

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        data["id"] = 1
        data["description"]=descriptionpreprocessing(data["description"])
        # print(data["description"])
        # print(folder)

    # folder_path = os.path.join(BASE_PATH, "querry")
    # картинки
    images = process_ad_images(Path("querry"))
    images.reshape(-1)
    data["images"] = images  # 👈 добавляем массив

    rows.append(data)
    df = pd.DataFrame(rows)
    # df = df.join(pd.DataFrame(df["images"].tolist()).add_prefix("images_"))
    # df = df.drop(columns=["images"])
    # df.columns = data1.columns
    row = df.iloc[0]

    row_df = row.to_frame().T.reindex(columns=data1.columns)

    df = pd.concat([data1, row_df], ignore_index=True)[1:]
    # print(df)
    # df.to_json("datatest.json", orient="records", indent=2, force_ascii=False)
    # exit()



    # df["Suprafață totală"] = df["Suprafață totală"].str.extract(r"(\d+)").astype(float)
    # df["Suprafață locativă"] = df["Suprafață locativă"].str.extract(r"(\d+)").astype(float)
    df["Suprafață totală"] = (
        pd.to_numeric(
            df["Suprafață totală"].astype(str).str.extract(r"(\d+)")[0],
            errors="coerce"
        )
        .fillna(0)
    )
    df["Suprafață locativă"] = (
        pd.to_numeric(
            df["Suprafață locativă"].astype(str).str.extract(r"(\d+\.?\d*)")[0],
            errors="coerce"
        )
        .fillna(0)
    )
    df["Suprafață bucătărie"] = (
        pd.to_numeric(
            df["Suprafață bucătărie"].astype(str).str.extract(r"(\d+)")[0],
            errors="coerce"
        )
        .fillna(0)
    )
    df["Inălțimea tavanelor"] = (
        pd.to_numeric(
            df["Inălțimea tavanelor"].astype(str).str.extract(r"(\d+)")[0],
            errors="coerce"
        )
        .fillna(0)
    )
    # df["Suprafață bucătărie"] = df["Suprafață bucătărie"].str.extract(r"(\d+)").astype(float)
    # df["Inălțimea tavanelor"] = df["Inălțimea tavanelor"].str.extract(r"(\d+)").astype(float)
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
    df[cols] = df[cols].apply(pd.to_numeric)
    df["Număr de camere"] = (
        df["Număr de camere"]
        .str.extract(r"(\d+)")
        .astype("float")   # сначала float (из-за NaN)
        .astype("Int64")   # nullable int
    )
    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].fillna(0)
    df = pd.concat([
        df.reset_index(drop=True),
        pd.DataFrame(df["images"].tolist()).add_prefix("images_")
    ], axis=1)
    df = pd.concat([
        df.reset_index(drop=True),
        pd.DataFrame(df["description"].tolist()).add_prefix("description_")
    ], axis=1)
    df = df.drop(columns=["description", "images"])


    df = pd.get_dummies(
        df,
        columns=["Autorul anunțului", "Living", "Fond locativ", "Dezvoltator", "Starea apartamentului", "Compartimentare", "Loc de parcare", "Tip clădire", "Copii", "Animale"],
        drop_first=False,
        dtype=int
    )




    df1 = pd.read_json("datacolumnsfin.json")
    row = df.iloc[0]

    row_df = row.to_frame().T.reindex(columns=df1.columns)

    df = pd.concat([df1, row_df], ignore_index=True)[1:]
    df.to_json("datatest.json", orient="records", indent=2, force_ascii=False)
    df.fillna(0, inplace=True)
    model = joblib.load("model.pkl")
    x = df.drop(columns=["id", "price"])
    y = abs(model.predict(x))
    print(y)


    print(df)

    return y