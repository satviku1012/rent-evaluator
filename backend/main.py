from fastapi import FastAPI
from backend.schemas import PredictRequest, PredictResponse
from backend.model import RentModel
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd

from backend.db import init_db
from backend.db import get_connection
from backend.db import save_prediction_to_db

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

rent_model = RentModel()

@app.on_event("startup")
def startup() -> None:
    rent_model.load()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    features = payload.dict()
    fair_rent = rent_model.predict_rent(features)
    mae = rent_model.mae
    range_low = int(fair_rent - mae)
    range_high = int(fair_rent + mae)
    delta = payload.asking_rent - fair_rent
    verdict = "overpriced" if delta > 100 else "underpriced" if delta < -100 else "fair"

    top_factors = [
        "Zip code affects baseline rent",
        "Square footage shifts expected price",
        "Bedrooms, bathrooms, and amenities adjust the estimate",
    ]

    prediction = {
        **features,
        "fair_rent": int(fair_rent),
        "range_low": range_low,
        "range_high": range_high,
        "delta": int(delta),
        "verdict": verdict,
        "top_factors": top_factors,
    }

    # Save to Postgres
    save_prediction_to_db(prediction)

    return PredictResponse(**prediction)

@app.get("/analytics")
def analytics():
    query = """
    SELECT zip_code, 
           AVG(fair_rent) AS avg_fair_rent, 
           COUNT(*) AS num_predictions,
           AVG(delta) AS avg_delta
    FROM predictions
    GROUP BY zip_code
    ORDER BY zip_code
    """
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query)
        results = cur.fetchall()
    conn.close()

    # Return JSON
    return {
        "by_zip_code": [
            {"zip_code": r["zip_code"], "avg_fair_rent": float(r["avg_fair_rent"]), 
             "num_predictions": r["num_predictions"], "avg_delta": float(r["avg_delta"])}
            for r in results
        ]
    }

