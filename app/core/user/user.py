from dataclasses import dataclass


@dataclass
class User:
    name: str
    api_key: str


@dataclass
class BitcoinWallet:
    address: str
    balance: float
    user_id: int
