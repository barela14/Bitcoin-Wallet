from fastapi import APIRouter, Depends

from app.core.facade import BitcoinWalletService
from app.infra.fastapi.dependables import get_core
from app.infra.fastapi.responses import CreateWalletResponse

user_api = APIRouter(prefix="/user", tags=["User"])


@user_api.post(path="/wallets{api_key}")
def create_wallet(
    api_key: str, core: BitcoinWalletService = Depends(get_core)
) -> CreateWalletResponse:
    return core.create_wallet(api_key)
