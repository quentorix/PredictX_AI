# 🏠 PredictX AI — Multimodal Apartment Price Estimator

**PredictX AI** is a high-performance desktop application engineered for precise real estate valuation in the Republic of Moldova. By moving beyond traditional calculators, this system implements a **Multimodal Fusion** architecture, synergizing tabular data, deep visual analysis of interior photos, and semantic processing of listing descriptions.

---

## 🎯 Market Relevance & Problem Statement
The real estate market in Moldova often suffers from subjective pricing and a lack of transparency. Sellers often overprice due to emotional attachment, while buyers lack the tools to verify market fairness.

**PredictX AI solves this by:**
*   **Data-Driven Objectivity:** Leveraging a massive dataset of **23,353 real listings** scraped from **999.md**, the country's leading marketplace.
*   **Visual Condition Audit:** Traditional models ignore renovation quality. Our AI uses Computer Vision to "see" the apartment quality, lighting, and layout signals.
*   **Semantic Understanding:** Natural Language Processing (NLP) identifies hidden value drivers (e.g., "new plumbing", "panoramic view") within the raw text of descriptions.

---

## 🚀 Key Features
*   **Multimodal AI Fusion:** A hybrid architecture combining Gradient Boosting (XGBoost/LightGBM), Computer Vision (CLIP), and NLP (SentenceTransformers).
*   **Modern Fintech UI:** A sleek, user-friendly desktop interface built with **CustomTkinter**, featuring real-time correlation heatmaps and transparent result cards.
*   **Asynchronous Engine:** Multi-threaded processing ensures the UI remains responsive while heavy AI inference runs in the background.
*   **Accuracy Metrics:** The model achieves a **Mean Absolute Error (MAE) of ~€16,012** and an **R² Score of 0.82**, indicating high reliability for market-average properties.

---

## 🛠 Technical Stack
*   **Framework:** CustomTkinter (Python Desktop)
*   **Computer Vision:** PyTorch & OpenAI CLIP (ViT-B/32)
*   **NLP:** SentenceTransformers (all-mpnet-base-v2 — 768d embeddings)
*   **Machine Learning:** XGBoost & LightGBM
*   **Data Processing:** Pandas, Scikit-learn, Numpy
*   **Web Scraping:** Playwright & BeautifulSoup4

---

## ⚙️ Installation & Environment Setup

To ensure the project runs smoothly, it is highly recommended to use a virtual environment to manage the ~80 specific dependencies.

### Step 1: Clone the Repository
```bash
git clone https://github.com/quentorix/PredictX_AI.git
cd PredictX_AI
Step 2: Create and Activate a Virtual Environment
Option A: Using Python venv (Standard)
```
# Create environment
```bash
python -m venv venv
```

# Activate for Windows:
```bash
.\venv\Scripts\activate
```


# Activate for Mac/Linux:
```
source venv/bin/activate
Option B: Using Conda
conda create --name predictx_env python=3.10
conda activate predictx_env
```
Step 3: Install Dependencies
This will install all required libraries (Torch, Transformers, XGBoost, CustomTkinter, etc.) with the exact versions used during development:
```
pip install --upgrade pip
pip install -r requirements.txt
```
Step 4: Download Pre-trained Models & Data
The trained model and dataset are stored externally due to file size.
[Download](https://drive.google.com/file/d/1uxrHZiYgFYY6UCNEniIx8vES8pShQ2D5/view)  and 
Place data123.json in the /data folder.
Place model.pkl in the /models folder.
Step 5: Launch the Application
python src/ui.py

--------------------------------------------------------------------------------
## 🏗 System Architecture
Image Branch: Multiple photos are processed via CLIP. We use Max-Pooling to merge embeddings from different rooms into a single visual state vector (512d).
Text Branch: Raw descriptions are encoded into a 768-dimensional semantic space using SentenceTransformers.
Tabular Branch: Technical specs (floor, area, building type) undergo One-Hot Encoding and normalization.
The Fusion: All vectors are concatenated and fed into an XGBoost Regressor to predict the final market price.

--------------------------------------------------------------------------------
## ⚖️ Ethics, Privacy & Safety
* Data Privacy: All scraped data is processed in aggregate. No personal contact information of sellers is stored or displayed.
* Bias Awareness: The model reflects historical market data. It is a decision-support tool, not a replacement for professional appraisal.
* Disclaimer: PredictX AI provides estimates. These results are not intended as final financial advice.

--------------------------------------------------------------------------------
## 👥 Target Audience
* Home Buyers: Instantly verify if a listing price is realistic.
* Sellers: Determine a competitive price based on 23,000 similar transactions.
* Real Estate Agents: Automate preliminary valuations for new client objects.

--------------------------------------------------------------------------------
