# Multimodal Emotion Analysis Setup

This project implements a multimodal emotion analysis system (Text + Image) using FastAPI and Streamlit.

## Components

1.  **Backend (FastAPI)**: `main.py`
    - Loads RoBERTa (Text) and DeepFace/CLIP (Image) models.
    - Exposes `POST /analyze_multimodal`.
    - Fuses results with weighted average.

2.  **Frontend (Streamlit)**: `app.py`
    - Provides a UI to input text and upload images.
    - Sends data to the backend API.
    - Visualize results.

## How to Run

You need to run **two separate terminals** to start the full system.

### Terminal 1: Backend Server
Start the FastAPI server. **Note:** The first run will be slow as it downloads DeepFace and CLIP models.

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run server
python main.py
```

Wait until you see: `Uvicorn running on http://0.0.0.0:8000`.

### Terminal 2: Frontend Client
Start the Streamlit app.

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run app
streamlit run app.py
```

Open your browser to the URL shown (usually `http://localhost:8501`).

## Troubleshooting

- **Node.js**: The Next.js frontend could not be created because Node.js is missing on your system. Streamlit is used as a robust alternative.
- **Model Downloads**: If the backend seems stuck, check the terminal. It might be downloading large model files (DeepFace weights, CLIP model). This only happens once.
