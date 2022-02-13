from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    name: str
    api_key: str


@dataclass
class BitcoinWallet:
    address: str
    balance: float
    user_id: Optional[int] = None
