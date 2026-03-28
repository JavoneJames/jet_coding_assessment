from pydantic import BaseModel
from typing import List, Dict

from pydantic.root_model import RootModel

class RestaurantModel(BaseModel):
    name: str
    cuisines: List[str]
    rating: float
    address: str

class RestaurantData(RootModel):
    Dict[int, RestaurantModel]
