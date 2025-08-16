from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    username: str
    email: str
    phone_number: str
    location: str


@dataclass
class Transaction:
    amount: int
    payment_method: str = ""
    callback_url: str = ""
    currency: str = "KES"
    narration: str = ""
    provider: str = ""
    channel: str = ""
    business_account: str = ""
    business_number: str = ""
    trans_type: str = ""
