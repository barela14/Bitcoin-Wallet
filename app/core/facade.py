from dataclasses import dataclass

from app.core.registration.interactor import RegistrationInteractor
from app.core.repository import IRepository
from app.core.user.interactor import UserInteractor
from app.infra.fastapi.responses import (
    CreateWalletResponseWrapper,
    RegistrationResponse,
)


@dataclass
class BitcoinWalletService:
    register_interactor: RegistrationInteractor
    user_iteractor: UserInteractor

    def register_user(self, user_name: str) -> RegistrationResponse:
        return self.register_interactor.register_user(user_name)

    def create_wallet(self, api_key: str) -> CreateWalletResponseWrapper:
        return self.user_iteractor.create_wallet(api_key)

    @classmethod
    def create(cls, repository: IRepository) -> "BitcoinWalletService":
        return cls(
            register_interactor=RegistrationInteractor(repository),
            user_iteractor=UserInteractor(repository),
        )
