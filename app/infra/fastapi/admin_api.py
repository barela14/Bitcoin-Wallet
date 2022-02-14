from fastapi import APIRouter, Depends

from app.core.facade import BitcoinWalletService
from app.infra.fastapi.dependables import get_core
from app.infra.fastapi.responses import GetStatisticsResponse

uid = "admin"
admin_api = APIRouter(prefix=f"/{uid}", tags=[uid])


@admin_api.post(path="/statistics")
def get_statistics(
    admin_api_key: str, core: BitcoinWalletService = Depends(get_core)
) -> GetStatisticsResponse:
    return core.get_statistics(admin_api_key)
