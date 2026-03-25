import pytest # type: ignore
# from find_restaurant_data.fetch_data_by_postcode import get_postcode_data 
from find_restaurant_data.fetch_data_by_postcode import validate_postcode, get_postcode_data, check_response_status_code, filter_received_data, extract_relevant_data_points

def test_validate_postcode():
    assert validate_postcode("EC4M7RF") == True
    assert validate_postcode("12344") == False
    assert validate_postcode("NE97YT") == True
    assert validate_postcode("") == False
    assert validate_postcode(None) == False

def test_check_response_status_code():
    pass

def test_get_postcode_data():
    pass

def test_filter_received_data():
    pass

def test_extract_relevant_data_points():
    pass

# def test():
#     print(pytest.__version__)

