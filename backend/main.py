from backend.post_code_api import POST_CODE_API
from backend.models.restaurant_data_model import RestaurantData
from backend.utils.check_postcode_is_real import check_postcode_is_real

from fastapi import Depends, FastAPI, HTTPException, Request
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
pc_api = POST_CODE_API()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="frontend")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/validate-postcode/{postcode}")
def validate_postcode(postcode: str = Depends(check_postcode_is_real)):
    return postcode

@app.get("/restaurants/{postcode}", response_model=RestaurantData)
def get_restaurants(postcode: str = Depends(validate_postcode)):
    try:
        restaurants_data = pc_api.fetch_filter_extract_restaurants(postcode)
        validated_data = RestaurantData.model_validate(restaurants_data)
        return validated_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
