🏠 PredictX AI — Multimodal Apartment Price Estimator
PredictX AI is a high-performance desktop application designed for precise real estate valuation. Unlike traditional calculators, this system employs a multimodal approach, merging tabular data, deep visual analysis of property photos, and semantic processing of descriptions.

🚀 Key Features
Multimodal AI Fusion: A hybrid architecture combining Classical ML (Scikit-learn), Computer Vision (ResNet18), and Natural Language Processing (SentenceTransformers).

Visual Condition Audit: The engine extracts embeddings from interior/exterior photos to account for renovation quality, lighting, and layout signals.

Semantic NLP Analysis: Processes listing descriptions to detect hidden value drivers that numbers alone can't capture.

Asynchronous Processing: Utilizes Python threading to ensure a smooth UI experience—the app displays a "Processing" state while the heavy AI inference runs in the background.

Modern Fintech UI: A sleek, user-friendly interface built with CustomTkinter.

🛠 Tech Stack
Framework: CustomTkinter

Computer Vision: PyTorch & Torchvision (Pre-trained ResNet18)

NLP: SentenceTransformers (all-MiniLM-L6-v2)

Data Science: Pandas, Numpy, Scikit-learn

Model Management: Joblib

📦 How It Works
To launch the programm you need to copy everuthing from src folder, instal required libraries and launch ui.py.
Data Collection: Users upload apartment photos and input technical specifications (area, floor, location, etc.).

Input Validation: A built-in validator ensures no critical fields are left blank before triggering the AI.

The Pipeline:

Images: Photos are transformed and passed through ResNet18 to generate 512-dimensional feature vectors.

Text: The description is encoded into a 384-dimensional semantic embedding.

Tabular: Features are cleaned, normalized, and one-hot encoded.

Inference: The fused feature vector is fed into a trained Regression model to predict the final market price.
