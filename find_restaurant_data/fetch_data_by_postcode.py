import requests
import re
POST_CODE = "EC4M7RF"

# check if the postcode is valid based on UK format
def validate_postcode(postcode: str) -> bool:
    if not postcode or not isinstance(postcode, str):
        return False
    pattern = (
        r"^("  
        r"GIR 0AA|"  # Special postcode
        r"(?:[A-PR-UWYZ][0-9][0-9A-HJKSTUW]?|"             # A9, A9A
        r"[A-PR-UWYZ][A-HK-Y][0-9][0-9ABEHMNPRV-Y]?))"     # AA9, AA9A
        r"\s?[0-9][ABD-HJLNP-UW-Z]{2}$"                    # Inward code
    )    
    return bool(re.match(pattern=pattern, string=postcode))
# send a 'get' requests ot the api using a postcode
def get_postcode_data():
    pass

# check response status code
def check_response_status_code():
    pass

# filter the received data to focus on restaurant data
def filter_received_data():
    pass

# from these restaurant object extract Name, Cuisines, Rating -as a number, and Address
def extract_relevant_data_points():
    pass

print(validate_postcode(POST_CODE))
