import random
import string
from dataclasses import dataclass
from typing import Callable

from app.core.repository import IRepository
from app.infra.fastapi.responses import CreateWalletResponse, Response


def simple_adress_generator(arg: str) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))


@dataclass
class UserInteractor:
    repository: IRepository
    starting_deposit: float = 1.0
    address_fn: Callable[[str], str] = simple_adress_generator

    def create_wallet(self, api_key: str) -> CreateWalletResponse:
        user_id = self.repository.get_user_id_by_api_key(api_key)
        wallets = self.repository.get_wallets_by_user_id(user_id)

        if len(wallets) >= 3:
            return Response()
        address = self.address_fn("")
        self.repository.create_wallet(address, self.starting_deposit, api_key)

        return CreateWalletResponse(address, self.starting_deposit, 7)
