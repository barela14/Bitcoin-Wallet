from dataclasses import dataclass
from typing import Optional

from app.core.user.user import BitcoinWallet

SUCCESS_CODE = 0
FAILURE_CODE = 1

SUCCESS_MESSAGE = "SUCCESS"
FAILURE_MESSAGE = "FAILURE"


@dataclass
class Response:
    status_code: int = SUCCESS_CODE
    status_message: str = SUCCESS_MESSAGE


# T = TypeVar("T")
#
#
# @dataclass
# class Result(Generic[T]):
#     object: T
#     response: Response


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
class BitcoinWalletWrapper:
    address: str
    balance_bitcoin: float
    balance_usd: float


@dataclass
class CreateWalletResponseWrapper:
    status_code: int
    status_message: str
    args: Optional[BitcoinWalletWrapper] = None


# class WalletResponseWrapper:
#     response: Optional[CreateWalletResponse]
#     error: Optional[Response]
