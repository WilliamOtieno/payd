import base64
import logging

import requests

from payd.models import Transaction, User

logger: logging.Logger = logging.getLogger(__name__)


class PaydClient:

    def __init__(self, username, password):
        self.acc_username = username
        self.acc_password = password

    def build_auth_headers(self) -> dict:
        creds = f"{self.acc_username}:{self.acc_password}"
        encoded_creds = base64.b64encode(creds.encode())
        return {"Authorization": f"Basic {encoded_creds.decode()}"}

    def trigger_card_payment(self, user: User, transaction: Transaction) -> dict:
        url = "https://api.mypayd.app/api/v1/payments"
        paylod = {
            "amount": transaction.amount,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "location": user.location,
            "username": user.username,
            "payment_method": transaction.payment_method,
            "provider": transaction.provider,
            "callback_url": transaction.callback_url,
            "reason": transaction.narration,
            "phone": user.phone_number,
        }
        headers = self.build_auth_headers()
        response = requests.post(url, data=paylod, headers=headers)
        if not response.ok:
            logger.error(f"{response.status_code}: {response.text}")
            if not response.json():
                return {}
        return response.json()

    def trigger_p2p_payment(self, user: User, transaction: Transaction) -> dict:
        url = "https://api.mypayd.app/api/v2/p2p"
        paylod = {
            "amount": transaction.amount,
            "receiver_username": user.username,
            "narration": transaction.narration,
            "phone_number": user.phone_number,
        }
        headers = self.build_auth_headers()
        response = requests.post(url, data=paylod, headers=headers)
        if not response.ok:
            logger.error(f"{response.status_code}: {response.text}")
            if not response.json():
                return {}
        return response.json()

    def trigger_payment_request(self, user: User, transaction: Transaction) -> dict:
        url = "https://api.mypayd.app/api/v2/payments"
        paylod = {
            "username": user.username,
            "channel": "MPESA",
            "amount": transaction.amount,
            "phone_number": user.phone_number,
            "narration": transaction.narration,
            "currency": transaction.currency,
            "callback_url": transaction.callback_url,
        }
        headers = self.build_auth_headers()
        response = requests.post(url, data=paylod, headers=headers)
        if not response.ok:
            logger.error(f"{response.status_code}: {response.text}")
            if not response.json():
                return {}
        return response.json()

    def trigger_paybill_request(self, user: User, transaction: Transaction) -> dict:
        url = "https://api.mypayd.app/api/v3/withdrawal"
        paylod = {
            "username": user.username,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "phone_number": user.phone_number,
            "narration": transaction.narration,
            "transaction_channel": "bank",
            "channel": "bank",
            "business_account": transaction.business_account,
            "business_number": transaction.business_number,
            "callback_url": transaction.callback_url,
        }
        headers = self.build_auth_headers()
        response = requests.post(url, data=paylod, headers=headers)
        if not response.ok:
            logger.error(f"{response.status_code}: {response.text}")
            if not response.json():
                return {}
        return response.json()

    def trigger_till_request(self, user: User, transaction: Transaction) -> dict:
        url = "https://api.mypayd.app/api/v3/withdrawal"
        paylod = {
            "username": user.username,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "phone_number": user.phone_number,
            "narration": transaction.narration,
            "transaction_channel": "bank",
            "channel": "bank",
            "business_account": transaction.business_account,
            "callback_url": transaction.callback_url,
        }
        headers = self.build_auth_headers()
        response = requests.post(url, data=paylod, headers=headers)
        if not response.ok:
            logger.error(f"{response.status_code}: {response.text}")
            if not response.json():
                return {}
        return response.json()

    def trigger_widthrawal_request(self, user: User, transaction: Transaction) -> dict:
        url = "https://api.mypayd.app/api/v2/withdrawal"
        paylod = {
            "amount": transaction.amount,
            "phone_number": user.phone_number,
            "narration": transaction.narration,
            "callback_url": transaction.callback_url,
            "channel": "MPESA",
        }
        headers = self.build_auth_headers()
        response = requests.post(url, data=paylod, headers=headers)
        if not response.ok:
            logger.error(f"{response.status_code}: {response.text}")
            if not response.json():
                return {}
        return response.json()

    def query_transaction(self) -> dict:
        url = "https://api.mypayd.app/api/v1/accounts/transaction-requests"
        payload = {}
        headers = self.build_auth_headers()
        response = requests.get(url, headers=headers, data=payload)
        if not response.ok:
            logger.error(f"{response.status_code}: {response.text}")
            if not response.json():
                return {}
        return response.json()

    def query_transaction_cost(self, transaction: Transaction) -> dict:
        """
        trans_type : withdrawal/receipt/remittance
        channel : mobile/bank/card/payd
        """
        url = "https://api.mypayd.app/api/v1/transaction-costs"
        params = {
            "amount": transaction.amount,
            "type": transaction.trans_type,
            "channel": transaction.channel,
        }
        headers = self.build_auth_headers()
        response = requests.get(url, headers=headers, params=params)
        if not response.ok:
            logger.error(f"{response.status_code}: {response.text}")
            if not response.json():
                return {}
        return response.json()
