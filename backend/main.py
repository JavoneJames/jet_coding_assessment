from fastapi import FastAPI
from backend.post_code_api import API_URL, POST_CODE, POST_CODE_API

app = FastAPI()
pc_api = POST_CODE_API()

@app.get("/restaurants")
def read_root():
    pc_api.validate_postcode(POST_CODE)
    received_data = pc_api.get_postcode_data(API_URL, POST_CODE)
    filtered_data = pc_api.filter_received_data(received_data)
    restaurants_data = pc_api.extract_relevant_data_points(filtered_data)
    return pc_api.print_restaurants_info(restaurants_data)
