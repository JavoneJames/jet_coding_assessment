from pydantic import BaseModel
from typing import List, Dict

class RestaurantModel(BaseModel):
    name: str
    cuisines: List[str]
    rating: float
    address: str

class RestaurantData(BaseModel):
    __root__: Dict[int, RestaurantModel]
