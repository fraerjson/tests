import requests


class EventPlaygroundService:
    limit = 5
    base_url = "http://localhost:8000/api/"

    def check_availability(self):
        response = requests.get(f"{self.base_url}ping/")
        response.raise_for_status()

    def create_user(self, user_data: dict):
        response = requests.post(f"{self.base_url}users/", json=user_data)
        response.raise_for_status()
        return response.json()

    def authorization(self, authorization_data: dict):
        query_params = dict(phone_number=authorization_data['phone_number'], password=authorization_data['password'])
        response = requests.get(f"{self.base_url}authorization/", query_params)
        response.raise_for_status()
        return response.json()

    def check_name(self, name_data: dict):
        query_params = dict(name=name_data['name'])
        response = requests.get(f"{self.base_url}name/", query_params)
        response.raise_for_status()
        return response.json()

    def check_phone_number(self, phone_number_data: dict):
        query_params = dict(phone_number=phone_number_data['phone_number'])
        response = requests.get(f"{self.base_url}phone_number/", query_params)
        response.raise_for_status()
        return response.json()

    def get_users_id(self, user_data):
        query_params = dict(tg_id=user_data['tg_id'])
        response = requests.get(f"{self.base_url}tg_id/", params=query_params)
        response.raise_for_status()
        return response.json()


    def post_user_pk(self, user_data: dict, user_id):
        response = requests.put(f"{self.base_url}users/{user_id['id']}", json=user_data)
        response.raise_for_status()
        return response.json()

    def post_wallet(self, user_data):
        response = requests.post(f"{self.base_url}wallets/", json=user_data)
        response.raise_for_status()
        return response.json()


    def transactions_transfer_id(self, user_data):
        pass
    
    


event_service = EventPlaygroundService()