from typing import List, Optional, Protocol

from app.core.user.user import BitcoinWallet, User
from app.infra.fastapi.responses import CreateWalletResponse


class IRepository(Protocol):
    def register_user(self, user: User) -> None:
        pass

    def create_wallet(
        self, address: str, starting_deposit: float, api_key: str
    ) -> CreateWalletResponse:
        pass

    def get_wallets_by_user_id(self, user_id: int) -> List[BitcoinWallet]:
        pass

    def get_user_id_by_api_key(self, api_key: str) -> Optional[int]:
        pass
