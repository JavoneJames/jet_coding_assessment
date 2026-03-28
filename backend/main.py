from fastapi import FastAPI
from backend.post_code_api import POST_CODE, POST_CODE_API
from backend.models.restaurant_data_model import RestaurantModel

app = FastAPI()
pc_api = POST_CODE_API()

@app.get("/restaurants")
def read_root():
    pc_api.validate_postcode(POST_CODE)
    received_data = pc_api.get_postcode_data(POST_CODE)
    filtered_data = pc_api.filter_received_data(received_data)
    restaurants_data = pc_api.extract_relevant_data_points(filtered_data)
    return restaurants_data 


@app.get("/restaurants/cuisines_types")
def get_by_cuisines():
    pc_api.validate_postcode(POST_CODE)
    received_data = pc_api.get_postcode_data(POST_CODE)
    filtered_data = pc_api.filter_received_data(received_data)
    restaurants_data = pc_api.extract_relevant_data_points(filtered_data, "Burgers")
    return restaurants_data 

@app.get("/restaurants/ratings")
def get_by_ratings():
    pc_api.validate_postcode(POST_CODE)
    received_data = pc_api.get_postcode_data(POST_CODE)
    filtered_data = pc_api.filter_received_data(received_data)
    restaurants_data = pc_api.extract_relevant_data_points(filtered_data, rating=4)
    return restaurants_data 

