from starlette.requests import Request

from app.core.facade import BitcoinWalletService


def get_core(request: Request) -> BitcoinWalletService:
    core: BitcoinWalletService = request.app.state.core
    return core
