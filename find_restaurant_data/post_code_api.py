import requests
import re

POST_CODE = "EC4M7RF"
API_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/"

user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36"
headers = {"User-Agent": user_agent}

class POST_CODE_API:

    # check if the postcode is valid based on UK format
    def validate_postcode(self, postcode: str):
        if not postcode or not isinstance(postcode, str):
            raise ValueError(f"Invalid postcode: {postcode}")        
        pattern = (
            r"^("
            r"GIR 0AA|"  # Special postcode
            r"(?:[A-PR-UWYZ][0-9][0-9A-HJKSTUW]?|"  # A9, A9A
            r"[A-PR-UWYZ][A-HK-Y][0-9][0-9ABEHMNPRV-Y]?))"  # AA9, AA9A
            r"\s?[0-9][ABD-HJLNP-UW-Z]{2}$"  # Inward code
        )
        if not re.match(pattern=pattern, string=postcode):
            raise ValueError(f"Invalid postcode format: {postcode}")
        
    # send a 'get' requests ot the api using a postcode
    def get_postcode_data(self, url: str, postcode: str) -> dict:
        self.validate_postcode(postcode)
        try:
            response = requests.get(url=f"{url}{postcode}", headers=headers)
            if not self.check_response_status_code(response.status_code):
                raise RuntimeError(f"Invalid status code: {response.status_code}")
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"API request failed: {e}")

    # check response status code
    def check_response_status_code(self, status) -> bool:
        return status == 200

    # filter the received data to focus on restaurant data
    def filter_received_data(self, data: dict) -> list:
        restaurants = data.get("restaurants")
        if not restaurants:
            raise ValueError("Restaurant object is empty")
        return restaurants

    # from these restaurant object extract Name, Cuisines, Rating -as a number, and Address
    def extract_relevant_data_points(self, filtered_restaurants_data: list) -> dict:
        extracted_data_points = {}
        for restaurant in filtered_restaurants_data:
            id = restaurant.get("id")
            cuisines = [cuisine for cuisine in restaurant.get("cuisines")]
            rating = restaurant.get("rating").get("starRating")
            address = restaurant.get("address")
            full_address = ", ".join(
                part
                for part in [
                    address.get("firstLine"),
                    address.get("city"),
                    address.get("postCode"),
                ]
                if part
            )

            extracted_data_points[id] = {
                "name": restaurant.get("name"),
                "cuisines": cuisines,
                "rating": rating,
                "address": full_address,
            }

            if len(extracted_data_points) == 10:
                break

        return extracted_data_points

if  __name__ == '__main__':
    pc_api = POST_CODE_API()
    data = pc_api.get_postcode_data(API_URL, POST_CODE)
    filtered_data = pc_api.filter_received_data(data)
    temp = pc_api.extract_relevant_data_points(filtered_data)
    print(temp)
