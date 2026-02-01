from pydantic import BaseModel
from typing import List

class PredictRequest(BaseModel):
    zip_code: int
    beds: int
    baths: float
    sqft: int

    parking: bool
    in_unit_laundry: bool
    pet_friendly: bool
    utilities_included: bool

    asking_rent: int

class PredictResponse(BaseModel):
    fair_rent: int
    range_low: int
    range_high: int
    delta: int
    verdict: str
    top_factors: List[str]