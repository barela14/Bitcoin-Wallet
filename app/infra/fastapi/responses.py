from dataclasses import dataclass

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
    address: str
    bitcoin_balance: float
    dollar_balance: float
