import requests


class EventPlaygroundService:
    limit = 5
    base_url = "http://localhost:8000/api/"

    def check_availability(self):
        response = requests.get(f"{self.base_url}ping/")
        response.raise_for_status()

    def authorization(self, authorization_data: dict):
        query_params = dict(phone_number=authorization_data['phone_number'], password=authorization_data['password'])
        response = requests.get(f"{self.base_url}authorization/", query_params)
        response.raise_for_status()
        return response.json()

    def check_register_name(self, name_data: dict):
        query_params = dict(name=name_data['name'])
        response = requests.get(f"{self.base_url}name/", query_params)
        response.raise_for_status()
        return response.json()

    def check_register_register_name(self, phone_number_data: dict):
        query_params = dict(phone_number=phone_number_data['phone_number'])
        response = requests.get(f"{self.base_url}phone_number/", query_params)
        response.raise_for_status()
        return response.json()

    def get_user_data_from_user_id(self, user_data):
        query_params = dict(tg_id=user_data['tg_id'])
        response = requests.get(f"{self.base_url}tg_id/", params=query_params)
        response.raise_for_status()
        return response.json()

    def get_user_data_from_user_wallet(self, user_data):
        query_params = dict(currency=user_data['currency'], users=user_data['users'])
        response = requests.get(f"{self.base_url}walletid/", params=query_params)
        response.raise_for_status()
        return response.json()

    def check_transaction_password(self, user_data):
        query_params = dict(password=user_data['password'], tg_id=user_data['tg_id'])
        response = requests.get(f"{self.base_url}password/", params=query_params)
        response.raise_for_status()
        return response.json()

    def find_wallet(self, user_data):
        query_params = dict(currency=user_data['currency'], users=user_data['users'])
        response = requests.get(f"{self.base_url}walletid/", params=query_params)
        response.raise_for_status()
        return response.json()

    def create_user(self, user_data: dict):
        response = requests.post(f"{self.base_url}users/", json=user_data)
        response.raise_for_status()
        return response.json()
    def patch_wallet(self, wallet_data):
        validate_wallet_data = {'amount': wallet_data['amount']}
        response = requests.patch(f"{self.base_url}walletid/{wallet_data['id']}", json=validate_wallet_data)
        validate_wallet_data = {'amount': wallet_data['recipient_amount']}
        response = requests.patch(f"{self.base_url}walletid/{wallet_data['recipient_id']}", json=validate_wallet_data)
        return response.json()

    def post_transactions(self, wallet_data):
        validate_wallet_data = {
            'currency': wallet_data['currency'],
            'recipient': wallet_data['recipient'],
            'sender': wallet_data['sender'],
            'amount_minus': wallet_data['amount_minus'],
            'wallet': wallet_data['wallet']}
        response = requests.post(f"{self.base_url}transactions/", json=validate_wallet_data)
        return response.json()


    def find_wallet_currency(self, user_data):
        currency = ["USD", "BTC", "ETH", "LIT", "BNB", "SOL", ]
        valid_currency = []
        for i in currency:
            query_params = dict(currency=i, users=user_data['users'])
            response = requests.get(f"{self.base_url}walletid/", params=query_params)
            if len(response.json()) == 1:
                valid_currency.append(i)
            else:
                pass
        return valid_currency


event_service = EventPlaygroundService()



event_service = EventPlaygroundService()