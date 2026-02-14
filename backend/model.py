import json
from pathlib import Path

import joblib
import pandas as pd


# Project-root-based paths so it works no matter where uvicorn is run from
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_DIR = PROJECT_ROOT / "ml" / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "model.joblib"
METADATA_PATH = ARTIFACT_DIR / "metadata.json"


class RentModel:
    def __init__(self) -> None:
        self.pipeline = None
        self.mae = None

    def load(self) -> None:
        self.pipeline = joblib.load(MODEL_PATH)

        with open(METADATA_PATH, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        self.mae = float(metadata["mae"])

    def predict_rent(self, features: dict) -> int:
        if self.pipeline is None:
            raise RuntimeError("Model is not loaded")

        df = pd.DataFrame([features])
        pred = self.pipeline.predict(df)[0]

        return int(round(pred))
