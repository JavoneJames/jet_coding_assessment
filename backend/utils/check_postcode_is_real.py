import requests

from fastapi import Depends
from backend.utils.validate_postcode import validate_postcode

def check_postcode_is_real(postcode: str = Depends(validate_postcode)):
    try:
        response = requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
        if response.status_code != 200:
                raise ValueError("postcode does not exists")
        return postcode
    except requests.RequestException as e:
        raise Exception(f"API request failed: {e}")
