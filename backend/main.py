from fastapi import FastAPI
from backend.schemas import PredictRequest, PredictResponse
from backend.model import RentModel

app = FastAPI()

rent_model = RentModel()

@app.on_event("startup")
def startup() -> None:
    rent_model.load()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict", response_model=PredictResponse)
def predict(data: PredictRequest):
    features = {
        "zip_code": int(data.zip_code),
        "beds": data.beds,
        "baths": data.baths,
        "sqft": data.sqft,
        "parking": int(data.parking),
        "in_unit_laundry": int(data.in_unit_laundry),
        "pet_friendly": int(data.pet_friendly),
        "utilities_included": int(data.utilities_included),
    }

    fair_rent = rent_model.predict_rent(features)
    mae = int(round(rent_model.mae))

    range_low = max(0, fair_rent - mae)
    range_high = fair_rent + mae

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
            "Zip code affects baseline rent",
            "Square footage shifts expected price",
            "Bedrooms, bathrooms, and amenities adjust the estimate",
        ],
    )
