from fastapi import APIRouter, Depends

from app.core.facade import BitcoinWalletService
from app.infra.fastapi.dependables import get_core
from app.infra.fastapi.responses import RegistrationResponse

uid = "register"

registration_api = APIRouter(prefix=f"/{uid}", tags=[uid])


@registration_api.post(path="/register/")
def register_user(
    user_name: str, core: BitcoinWalletService = Depends(get_core)
) -> RegistrationResponse:
    return core.register_user(user_name)
