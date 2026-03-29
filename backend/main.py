from fastapi import Depends, FastAPI, HTTPException, Request
from backend.post_code_api import POST_CODE_API
from backend.models.restaurant_data_model import RestaurantData
from backend.utils.validate_postcode import validate_postcode
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
pc_api = POST_CODE_API()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="frontend")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/restaurants/{postcode}")
def get_restaurants(postcode: str = Depends(validate_postcode)):
    try:
        received_data = pc_api.get_postcode_data(postcode)
        filtered_data = pc_api.filter_received_data(received_data)
        restaurants_data = pc_api.extract_relevant_data_points(filtered_data)
        return restaurants_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/restaurants/cuisines_types")
def get_by_cuisines(post_code: str, cuisine_type: str):
    received_data = pc_api.get_postcode_data(post_code)
    filtered_data = pc_api.filter_received_data(received_data)
    restaurants_data = pc_api.extract_relevant_data_points(
        filtered_data, cuisine_type=cuisine_type
    )
    return restaurants_data

@app.get("/restaurants/ratings")
def get_by_ratings(post_code: str, rating: int):
    received_data = pc_api.get_postcode_data(post_code)
    filtered_data = pc_api.filter_received_data(received_data)
    restaurants_data = pc_api.extract_relevant_data_points(filtered_data, rating=rating)
    return restaurants_data
