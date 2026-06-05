# 🛠 Technical Documentation: PredictX AI Architecture

This document provides an in-depth look at the multimodal machine learning pipeline used in PredictX AI to estimate real estate prices in Moldova.

## 1. Multimodal Fusion Architecture
PredictX AI utilizes a **late-fusion approach**, combining three distinct types of data inputs into a single feature vector for the final regression model.

### A. Visual Branch (Computer Vision)
*   **Model:** `openai/clip-vit-base-patch32` (CLIP).
*   **Process:** Interior and exterior photos are resized to 224x224 and normalized. CLIP extracts 512-dimensional feature vectors.
*   **Aggregation:** We use **Max-Pooling** to merge embeddings from multiple images of a single apartment into one representative visual state vector.

### B. Textual Branch (NLP)
*   **Model:** `sentence-transformers/all-mpnet-base-v2`.
*   **Process:** Listing descriptions from 999.md are cleaned using regex and encoded into a 768-dimensional semantic embedding.
*   **Handling Missing Data:** If no description is provided, a zero-vector is used to maintain input consistency.

### C. Tabular Branch (Structured Data)
*   **Features:** Floor, total area, number of rooms, building type, and construction year.
*   **Preprocessing:** 
    *   Numerical values are extracted via regex.
    *   Categorical features (e.g., "Building Type") undergo **One-Hot Encoding**.
    *   GPS coordinates (lat/long) are included to provide spatial context.

## 2. Regression Engine
The concatenated vector is processed by an **XGBoost Regressor**, selected for its superior performance over LightGBM in our tests.
*   **Hyperparameters:** 5000 estimators, learning rate of 0.01, and a max depth of 5.
*   **Current Metrics:** 
    *   MAE: ~€16,012
    *   R² Score: 0.82
    *   MAPE: 223% (Note: High percentage error is attributed to outlier listings on 999.md with €1 dummy prices).

## 3. Data Collection Pipeline
*   **Source:** Real-time scraping of **999.md**.
*   **Tools:** Playwright (browser automation) and BeautifulSoup4.
*   **Dataset:** 23,353 unique listings used for training and validation.

--------------------------------------------------------------------------------