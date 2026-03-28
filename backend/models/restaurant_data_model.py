from pydantic import BaseModel
from typing import List

class RestaurantModel(BaseModel):
    name: str
    cuisines: List[str]
    rating: float
    address: str

