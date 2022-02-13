import random
import string
from dataclasses import dataclass
from typing import Callable

from app.core.repository import IRepository
from app.infra.fastapi.responses import (
    BitcoinWalletWrapper,
    CreateWalletResponseWrapper,
)


def simple_adress_generator(arg: str) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


@dataclass
class UserInteractor:
    repository: IRepository
    starting_deposit: float = 1.0
    address_fn: Callable[[str], str] = simple_adress_generator

    def create_wallet(self, api_key: str) -> CreateWalletResponseWrapper:
        user_id = self.repository.get_user_id_by_api_key(api_key)
        if user_id is None:
            return CreateWalletResponseWrapper(1, "Wrong api_key")
        wallets = self.repository.get_wallets_by_user_id(user_id)
        if len(wallets) >= 3:
            return CreateWalletResponseWrapper(1, "Can't add any more wallets")

        address = self.address_fn("")
        wallet_result = self.repository.create_wallet(address, 1.0, api_key)

        args = wallet_result.args
        assert args is not None
        new_args = BitcoinWalletWrapper(args.address, args.balance, 7)
        return CreateWalletResponseWrapper(
            wallet_result.status_code, wallet_result.status_message, new_args
        )
