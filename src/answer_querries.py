
import numpy as np
import re
import nltk
from PIL import Image, ImageOps
from torchvision import models, transforms
import torch
from sentence_transformers import SentenceTransformer
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
import pandas as pd
from transformers import CLIPProcessor, CLIPModel
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
from pathlib import Path
import json
import joblib

BASE_PATH = "data"
IMG_SIZE = (224, 224)
device = "cuda" if torch.cuda.is_available() else "cpu"
data1 = pd.read_json("datacolumns.json")[:1]
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

clip_model.eval()
text_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def get_clip_image_embedding(image_path):
    img = Image.open(image_path).convert("RGB")

    inputs = clip_processor(
        images=img,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = clip_model.get_image_features(**inputs)

    if not isinstance(outputs, torch.Tensor):
        if hasattr(outputs, "image_embeds") and outputs.image_embeds is not None:
            outputs = outputs.image_embeds
        elif hasattr(outputs, "pooler_output") and outputs.pooler_output is not None:
            outputs = outputs.pooler_output
        elif hasattr(outputs, "last_hidden_state") and outputs.last_hidden_state is not None:
            outputs = outputs.last_hidden_state[:, 0, :]
        else:
            raise ValueError("Не найден tensor embedding в output CLIP")

    emb = outputs / outputs.norm(dim=-1, keepdim=True)

    return emb.cpu().numpy()[0]
def process_ad_images(folder_path):
    folder = Path(folder_path)
    embeddings = []

    for file in sorted(folder.iterdir()):
        if file.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            try:
                emb = get_clip_image_embedding(file)
                embeddings.append(emb)
            except Exception as e:
                print(f"Ошибка с картинкой {file}: {e}")


    if len(embeddings) == 0:
        return np.zeros(512)

    return np.max(embeddings, axis=0)

def descriptionpreprocessing(text):
    if text is None or str(text).strip() == "":
        return np.zeros(768)

    emb = text_model.encode(str(text), normalize_embeddings=True)

    embedding = text_model.encode(str(text))

    return embedding

path = Path("querry") / "data.json"

rows = []
i = 0
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)
    data["id"] = 1
    if not "description" in data:
        data["description"] = ""
    data["description"]=descriptionpreprocessing(data["description"])

images = process_ad_images(Path("querry"))
images.reshape(-1)
data["images"] = images  # 👈 добавляем массив

rows.append(data)
df = pd.DataFrame(rows)
row = df.iloc[0]

row_df = row.to_frame().T.reindex(columns=data1.columns)

df = pd.concat([data1, row_df], ignore_index=True)[1:]
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
    .astype("float")
    .astype("Int64")
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
df.columns = [
    re.sub(r'[^A-Za-z0-9_]+', '_', col)
    for col in df.columns
]
model = joblib.load("model.pkl")

X = df.drop(columns=["id", "price"])

X = X.replace([np.inf, -np.inf], np.nan)

X = X.apply(pd.to_numeric, errors="coerce")

X = X.fillna(0)

X = X.astype(np.float32)

y = abs(model.predict(X))
print(y)


print(df)