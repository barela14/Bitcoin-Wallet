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


@dataclass
class Transaction:
    user_id_from: str
    user_id_to: str
    wallet_address_from: str
    wallet_address_to: str
    amount: float

    def __hash__(self) -> int:
        return hash(
            (
                self.user_id_from,
                self.user_id_to,
                self.wallet_address_from,
                self.wallet_address_to,
                self.amount,
            )
        )
