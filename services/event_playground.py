import requests


class EventPlaygroundService:
    limit = 5
    base_url = "http://localhost:8000/api/"

    def check_availability(self):
        response = requests.get(f"{self.base_url}ping/")
        response.raise_for_status()

    def create_User(self, User_data: dict):
        response = requests.post(f"{self.base_url}User/", json=User_data)
        response.raise_for_status()
        return response.json()

    def authorization(self, authorization_data: dict):
        query_params = dict(phone_number=authorization_data['phone_number'], password=authorization_data['password'])
        response = requests.get(f"{self.base_url}authorization/", query_params)
        response.raise_for_status()
        return response.json()


event_service = EventPlaygroundService()