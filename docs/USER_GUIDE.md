# 📖 PredictX AI User Manual

Welcome to PredictX AI! This guide will help you navigate the application to get the most accurate price estimations for apartments in Moldova.

## Getting Started
1. **Launch the App:** Run python src/ui.py.
2. **Navigation:** Use the sidebar to switch between **Home**, **About**, **Analyze**, and **Estimate**.

## Step-by-Step Estimation
### 1. Upload Photos
*   Click **Select Files** on the "Estimate" screen.
*   **Pro Tip:** Upload at least 3-5 high-quality photos. Our AI analyzes the quality of the renovation, lighting, and layout.

### 2. Enter Specifications
*   **Main Parameters:** Provide the number of rooms, total area, and floor.
*   **Location:** Enter the GPS coordinates (Latitude/Longitude) for precision.
*   **Amenities:** Check the boxes for features like "Autonomous Heating", "Furnished", or "Elevator".
*   **Description:** Copy and paste the listing text. Our NLP engine looks for value keywords that numbers might miss.

### 3. Review Results
*   **Predicted Price:** The most likely market value in Euros.
*   **Confidence Score:** Based on the model's R² score (0.82), indicating how well the input data matches known market trends.
*   **Price Range:** A ±10% valuation bracket to account for market negotiations.
*   **Correlation Heatmap:** View how different factors (like area vs. price) interact in our dataset.

## Troubleshooting
*   **Missing Icons:** Ensure the `icons/` folder is present in the root directory.
*   **Model Not Loading:** Verify that `model.pkl` is located in the `/models` folder.

--------------------------------------------------------------------------------