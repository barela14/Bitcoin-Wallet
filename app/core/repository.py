from typing import List, Optional, Protocol

from app.core.user.user import BitcoinWallet, Transaction, User
from app.infra.fastapi.responses import (
    CreateWalletResponse,
    GetWalletResponse,
    Response,
)


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

    def get_wallet_by_address(self, address: str) -> GetWalletResponse:
        pass

    def update_wallet_balance(self, address: str, amount: float) -> Response:
        pass

    def register_transaction(
        self,
        address_from: str,
        address_to: str,
        amount: float,
        user_id_from: int,
        user_id_to: int,
    ) -> Response:
        pass

    def get_user_id_by_wallet_address(self, address: str) -> Optional[int]:
        pass

    def get_wallet_transactions_by_address(self, address: str) -> List[Transaction]:
        pass

    def get_number_of_transactions(self) -> int:
        pass

    def get_foreign_transactions_amount(self) -> float:
        pass
