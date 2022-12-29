import requests

global_currency ={
    'BTC': 16845,
    'ETH': 1220,
    'BNB': 243,
    'XRP': 0.35,
    'DOGE': 0.07,
    'ADA': 0.26,
}
class EventPlaygroundService:
    limit = 5
    base_url = "http://localhost:8000/api/"

    def check_availabiADAy(self):
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
        validate_wallet_data = {'amount': wallet_data['new_sender_amount']}
        response = requests.patch(f"{self.base_url}walletid/{wallet_data['sender_wallet_id']}", json=validate_wallet_data)
        validate_wallet_data = {'amount': wallet_data['new_recipient_amount']}
        response = requests.patch(f"{self.base_url}walletid/{wallet_data['recipient_wallet_id']}", json=validate_wallet_data)
        return response.json()

    def post_transactions(self, wallet_data):
        validate_wallet_data = {
            'sender': wallet_data['sender'],
            'sender_currency': wallet_data['sender_currency'],
            'send_amount': wallet_data['send_amount'],
            'recipient': wallet_data['recipient'],
            'recipient_currency': wallet_data['recipient_currency'],
            'received_amount': wallet_data['received_amount'],
            'commission': wallet_data['commission'],
            'wallet': wallet_data['sender_wallet_id']}
        response = requests.post(f"{self.base_url}transactions/", json=validate_wallet_data)
        return response.json()


    def find_wallet_currency(self, user_data):
        currency = ["USD", "BTC", "ETH", "ADA", "BNB", "XRP", "DOGE"]
        valid_currency = []
        query_params = dict(users=user_data['users'])
        response = requests.get(f"{self.base_url}walletid/", params=query_params)
        for i in response.json():
            valid_currency.append({'currency': i['currency'], 'amount': i['amount']})
        return valid_currency


event_service = EventPlaygroundService()



event_service = EventPlaygroundService()