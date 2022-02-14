from fastapi import APIRouter, Depends

from app.core.facade import BitcoinWalletService
from app.infra.fastapi.dependables import get_core
from app.infra.fastapi.responses import (
    CreateWalletResponseWrapper,
    GetTransactionResponse,
    GetWalletResponseWrapper,
    Response,
)

uid = "user"
user_api = APIRouter(prefix=f"/{uid}", tags=[uid])


@user_api.post(path="/wallets/")
def create_wallet(
    api_key: str, core: BitcoinWalletService = Depends(get_core)
) -> CreateWalletResponseWrapper:
    return core.create_wallet(api_key)


@user_api.get(path="/wallets/{address}")
def get_wallet(
    api_key: str, address: str, core: BitcoinWalletService = Depends(get_core)
) -> GetWalletResponseWrapper:
    return core.get_wallet(api_key, address)


@user_api.post(path="/transactions")
def make_transaction(
    api_key: str,
    address_from: str,
    address_to: str,
    amount: float,
    core: BitcoinWalletService = Depends(get_core),
) -> Response:
    return core.make_transaction(api_key, address_from, address_to, amount)


@user_api.get(path="/transactions")
def get_transactions(
    api_key: str, core: BitcoinWalletService = Depends(get_core)
) -> GetTransactionResponse:
    return core.get_transactions(api_key)


@user_api.get(path="/wallets/{address}/transactions")
def get_wallet_transactions(
    api_key: str, address: str, core: BitcoinWalletService = Depends(get_core)
) -> GetTransactionResponse:
    return core.get_wallet_transactions(api_key, address)
