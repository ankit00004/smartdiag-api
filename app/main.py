from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import numpy as np
import joblib
import os

app = FastAPI(title="SmartDiag API", version="1.0.0")

MODEL_PATH = os.getenv("MODEL_PATH", "model.pkl")

class PatientInput(BaseModel):
    features: List[float]

class PredictionOutput(BaseModel):
    prediction: int
    confidence: float
    label: str

LABELS = {0: "Healthy", 1: "At Risk", 2: "Critical"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PatientInput):
    try:
        model = joblib.load(MODEL_PATH)
        features = np.array(data.features).reshape(1, -1)
        prediction = int(model.predict(features)[0])
        confidence = float(model.predict_proba(features).max())
        return PredictionOutput(
            prediction=prediction,
            confidence=round(confidence, 4),
            label=LABELS.get(prediction, "Unknown")
        )
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Model not loaded")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics")
def metrics():
    """Basic observability endpoint for Prometheus scraping."""
    return {"uptime": "ok", "model_loaded": os.path.exists(MODEL_PATH)}
