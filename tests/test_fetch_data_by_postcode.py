import requests
import pytest  #type: ignore
from unittest.mock import patch, MagicMock

from find_restaurant_data.fetch_data_by_postcode import (
    validate_postcode,
    get_postcode_data,
    check_response_status_code,
    filter_received_data,
    extract_relevant_data_points,
)

API_URL = "http://fakeurl.com/"
POST_CODE = "SE1 9AD"
USER_AGENT = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36"
headers = {"User-Agent": USER_AGENT}

OBJECT_DATA = {
    "metaData": {},
    "restaurants": [],
    "deliveryFees": {},
    "promotedPlacement": [],
    "filters": {},
    "layout": {},
    "enrichedLists": [],
}

RECEIVED_DATA = {
    "metaData": {},
    "restaurants": [
        {
            "id": 1000,
            "name": f"Test Restaurant",
            "address": {
                "city": "London",
                "firstLine": "Example Street",
                "postCode": "SE1 9AD",
            },
            "rating": {
                "starRating": 5,
            },
            "cuisines": {
                "name": "sample",
            },
        }
    ],
    "deliveryFees": {},
    "promotedPlacement": {},
    "filters": {},
    "layout": {},
    "enrichedLists": [],
}

def test_validate_postcode():
    assert validate_postcode("EC4M7RF") == True
    assert validate_postcode("12344") == False
    assert validate_postcode("NE97YT") == True
    assert validate_postcode("") == False
    assert validate_postcode(None) == False

def test_check_response_status_code():
    assert check_response_status_code(200) is True
    assert check_response_status_code(401) is not True
    assert check_response_status_code(403) is not True
    assert check_response_status_code(408) is not True

def test_get_postcode_data():
    with patch("find_restaurant_data.fetch_data_by_postcode.validate_postcode", return_value=True), \
        patch("find_restaurant_data.fetch_data_by_postcode.check_response_status_code", return_value=True), \
        patch("find_restaurant_data.fetch_data_by_postcode.requests.get") as mock_get:

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = OBJECT_DATA
        mock_get.return_value = mock_response
        
        data = get_postcode_data(API_URL, POST_CODE)
        mock_get.assert_called_once_with(
            url=f"{API_URL}{POST_CODE}",
            headers=headers  
        )
        
        expected_keys = ['metaData', 'restaurants', 'deliveryFees', 'promotedPlacement', 'filters', 'layout', 'enrichedLists']
        assert set(data.keys()) == set(expected_keys)

def test_filter_received_data():
    with patch("find_restaurant_data.fetch_data_by_postcode.filter_received_data") as mock_filter:
        mock_filter.return_value = RECEIVED_DATA
        result = mock_filter(RECEIVED_DATA)
        mock_filter.assert_called_once_with(RECEIVED_DATA) 
        assert result == RECEIVED_DATA

def test_extract_relevant_data_points():
    with patch("find_restaurant_data.fetch_data_by_postcode.extract_relevant_data_points") as mock_extract:
        filtered_data = RECEIVED_DATA['restaurants']
        mock_extract.return_value = filtered_data 
        result = mock_extract(filtered_data)
        assert result == filtered_data
