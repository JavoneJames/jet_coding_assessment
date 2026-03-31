import requests
from fastapi import HTTPException
import pytest  # type: ignore
from unittest.mock import patch, MagicMock

from backend.post_code_api import POST_CODE_API
from backend.utils.validate_postcode import validate_postcode 

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

pc_api = POST_CODE_API()
pc_api.api_url = API_URL

def test_validate_postcode():
    assert validate_postcode("EC4M7RF") == "EC4M7RF"
    assert validate_postcode("NE97YT") == "NE97YT"
    
    with pytest.raises(HTTPException) as exc_info:
        validate_postcode("12344")
    assert exc_info.value.status_code == 400
    assert "Invalid postcode format" in str(exc_info.value.detail)
    
    with pytest.raises(HTTPException):
        validate_postcode("")

def test_check_response_status_code():
    assert pc_api.check_response_status_code(status=200)
    assert not pc_api.check_response_status_code(status=401)
    assert not pc_api.check_response_status_code(status=403)
    assert not pc_api.check_response_status_code(status=408)
    status =  pc_api.check_response_status_code(status=200)
    assert status != 404

def test_get_postcode_data():
    with (
        patch( "backend.utils.validate_postcode.validate_postcode", return_value=True),
        patch.object(
           POST_CODE_API, "check_response_status_code", return_value=True        ),
        patch("backend.post_code_api.requests.get") as mock_get,
    ):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = OBJECT_DATA
        mock_get.return_value = mock_response

        data = pc_api.get_postcode_data(postcode=POST_CODE)

        expected_keys = [
            "metaData",
            "restaurants",
            "deliveryFees",
            "promotedPlacement",
            "filters",
            "layout",
            "enrichedLists",
        ]
        assert set(data.keys()) == set(expected_keys)
        mock_get.assert_called_once_with(url=f"{API_URL}{POST_CODE}", headers=headers)

def test_filter_received_data():
    with patch.object(POST_CODE_API, "filter_received_data", return_value=RECEIVED_DATA) as mock_filter:
        mock_filter.return_value = RECEIVED_DATA
        result = mock_filter(RECEIVED_DATA)
        assert result == RECEIVED_DATA
        mock_filter.assert_called_once_with(RECEIVED_DATA)

def test_extract_relevant_data_points():
    filtered_data = RECEIVED_DATA["restaurants"]
    with patch.object(POST_CODE_API, "extract_relevant_data_points", return_value=filtered_data) as mock_extract:
        result = mock_extract(filtered_data)
        assert result == filtered_data
        mock_extract.assert_called_once_with(filtered_data)
