import os
import numpy as np

import nltk

from PIL import Image
from torchvision import transforms
import torch
from sentence_transformers import SentenceTransformer
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
from pathlib import Path
import json
import pandas as pd
from transformers import CLIPProcessor, CLIPModel

BASE_PATH = "data"
IMG_SIZE = (224, 224)
device = "cuda" if torch.cuda.is_available() else "cpu"

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

    return embedding  # shape: (384,)

path = "data_src"

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


    folder_path = os.path.join(BASE_PATH, folder)
    images = process_ad_images(folder_path)
    images.reshape(-1)
    data["images"] = images
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
    .astype("float")
    .astype("Int64")
)
num_cols = df.select_dtypes(include="number").columns
df[num_cols] = df[num_cols].fillna(0)
df = df.join(pd.DataFrame(df["images"].tolist()).add_prefix("images_"))
df = df.join(pd.DataFrame(df["description"].tolist()).add_prefix("description_"))
df = df.drop(columns=["description", "images"])


df = pd.get_dummies(
    df,
    columns=["Autorul anunțului", "Living", "Fond locativ", "Dezvoltator", "Starea apartamentului", "Compartimentare", "Loc de parcare", "Tip clădire", "Copii", "Animale"],
    drop_first=False,
    dtype=int
)

df.to_json("data123.json", orient="records", indent=2, force_ascii=False)
df[:1].to_json("datacolumnsfin.json", orient="records", indent=2, force_ascii=False)