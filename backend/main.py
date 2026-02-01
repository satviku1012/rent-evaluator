from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    # Placeholder logic (fake values for now)
    fair_rent = 1800
    range_low = 1700
    range_high = 1900
    delta = data.asking_rent - fair_rent

    if delta < -100:
        verdict = "underpriced"
    elif delta > 100:
        verdict = "overpriced"
    else:
        verdict = "fair"

    return PredictResponse(
        fair_rent=fair_rent,
        range_low=range_low,
        range_high=range_high,
        delta=delta,
        verdict=verdict,
        top_factors=[
            "Location adjustment based on zip code",
            "Square footage relative to market",
            "Bedroom and bathroom count",
        ],
    )