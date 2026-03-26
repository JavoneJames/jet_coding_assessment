import requests
import re

POST_CODE = "EC4M7RF"
API_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/"

user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36"
headers = {"User-Agent": user_agent}

# check if the postcode is valid based on UK format
def validate_postcode(postcode: str) -> bool:
    if not postcode or not isinstance(postcode, str):
        return False
    pattern = (
        r"^("
        r"GIR 0AA|"  # Special postcode
        r"(?:[A-PR-UWYZ][0-9][0-9A-HJKSTUW]?|"  # A9, A9A
        r"[A-PR-UWYZ][A-HK-Y][0-9][0-9ABEHMNPRV-Y]?))"  # AA9, AA9A
        r"\s?[0-9][ABD-HJLNP-UW-Z]{2}$"  # Inward code
    )
    return bool(re.match(pattern=pattern, string=postcode))

# check response status code
def check_response_status_code(status) -> bool:
    return status == 200

# send a 'get' requests ot the api using a postcode
def get_postcode_data(url: str, postcode: str) -> dict:
    if not validate_postcode(postcode):
        raise ValueError(f"Invalid postcode: {postcode}")
    try:
        response = requests.get(url=f"{url}{postcode}", headers=headers)
        if not check_response_status_code(response.status_code):
            raise RuntimeError(f"Invalid status code: {response.status_code}")
        return response.json()
    except requests.RequestException as e:
        raise Exception(f"API request failed: {e}")

# filter the received data to focus on restaurant data
def filter_received_data(data: dict) -> list:
    restaurants = data.get('restaurants')
    if not restaurants:
        raise ValueError("Restaurant object is empty")
    return restaurants

# from these restaurant object extract Name, Cuisines, Rating -as a number, and Address
def extract_relevant_data_points(filtered_data):
    pass 

data = get_postcode_data(API_URL, POST_CODE)
filtered_data = filter_received_data(data)
extract_relevant_data_points(filtered_data)
