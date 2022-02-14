from dataclasses import dataclass
from typing import List, Optional

from app.core.user.user import BitcoinWallet, Transaction

SUCCESS_CODE = 0
FAILURE_CODE = 1

SUCCESS_MESSAGE = "SUCCESS"
FAILURE_MESSAGE = "FAILURE"


@dataclass
class Response:
    status_code: int = SUCCESS_CODE
    status_message: str = SUCCESS_MESSAGE


@dataclass
class RegistrationResponse:
    name: str
    api_key: str


@dataclass
class CreateWalletResponse:
    status_code: int
    status_message: str
    args: Optional[BitcoinWallet] = None


@dataclass
class GetWalletResponse:
    status_code: int
    status_message: str
    args: Optional[BitcoinWallet] = None


@dataclass
class BitcoinWalletWrapper:
    address: str
    balance_bitcoin: float
    balance_usd: float


@dataclass
class CreateWalletResponseWrapper:
    status_code: int
    status_message: str
    args: Optional[BitcoinWalletWrapper] = None


@dataclass
class GetWalletResponseWrapper:
    status_code: int
    status_message: str
    args: Optional[BitcoinWalletWrapper] = None


@dataclass
class GetTransactionResponse:
    status_code: int
    status_message: str
    args: Optional[List[Transaction]] = None


@dataclass
class GetStatisticsResponse:
    status_code: int
    status_message: str
    num_transactions: Optional[int] = None
    total_profit: Optional[float] = None
