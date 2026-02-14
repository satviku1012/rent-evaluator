from pydantic import BaseModel
from typing import List, Literal

class PredictRequest(BaseModel):
    zip_code: Literal[
        53703, 53704, 53705, 53706, 53711, 53713,
        53714, 53715, 53716, 53717, 53718, 53719
    ]
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