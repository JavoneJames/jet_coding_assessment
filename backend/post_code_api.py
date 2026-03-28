import requests
import re
from math import floor
from backend.models import restaurant_data_model

POST_CODE = "EC4M7RF"
API_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/"

user_agent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36"
headers = {"User-Agent": user_agent}

NON_CUISINE_CATEGORIES = (
    "Beauty",
    "Convenience",
    "Collect stamps",
    "Flowers",
    "Shops",
    "Pharmacy",
    "Deals",
    "Lunch",
    "Freebies",
)


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
        try:
            response = requests.get(url=f"{url}{postcode.strip()}", headers=headers)
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
    
    # filter retrieved data by cuisine type
    def filter_by_cuisine(self, restaurants_data: list, cuisine_type:str) -> list:
        if not cuisine_type:
            return restaurants_data
        filtered_cuisines = []
        for restaurant in restaurants_data:
            for cuisine in restaurant.get("cuisines"):
                if cuisine["name"] == cuisine_type:
                    filtered_cuisines.append(restaurant)
        return filtered_cuisines
    
    def filter_by_rating(self, restaurants_data, rating: int):
        if not rating:
            return restaurants_data
        filtered_ratings = []
        for restaurant in restaurants_data:
            restaurant_rating = floor(restaurant.get("rating").get("starRating"))
            if restaurant_rating > rating:
                filtered_ratings.append(restaurant)
        return filtered_ratings

    # from these restaurant object extract Name, Cuisines, Rating -as a number, and Address
    def extract_relevant_data_points(self, filtered_restaurants_data: list, cuisine_type: str = None, rating: int = None) -> dict:
        filtered_data = self.filter_by_cuisine(filtered_restaurants_data, cuisine_type)
        filtered_data = self.filter_by_rating(filtered_restaurants_data, rating)
        extracted_data_points = {}
        for restaurant in filtered_data:
            id = restaurant.get("id")
            cuisines = [
                cuisine["name"]
                for cuisine in restaurant.get("cuisines")
                if cuisine["name"] not in NON_CUISINE_CATEGORIES
            ]
            rating = restaurant.get("rating").get("starRating")
            print(restaurant.get("address"))
            address = restaurant.get("address")
            full_address = ", ".join(
                part
                for part in [
                    address.get("firstLine"),
                    address.get("city"),
                    address.get("postalCode"),
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

    # print restaurants info to console
    def print_restaurants_info(self, restaurants_data):
        for restaurant in restaurants_data.values():
            print(f"Name: {restaurant['name']}")
            print(f"Cuisines: {', '.join(restaurant['cuisines'])}")
            print(f"Rating: {restaurant['rating']}")
            print(f"Address: {restaurant['address']}")
            print("-" * 40)

